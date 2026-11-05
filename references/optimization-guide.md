# C500 硬件感知算子优化

## 1. 先拆 stage，再算 Roofline

对每个 kernel/stage 分别计算：

```text
AI = FLOPs / compulsory_bytes
memory_roof_TFLOPS = AI × bandwidth_GBps / 1000
ridge_FLOP_per_B = compute_roof_TFLOPS × 1000 / bandwidth_GBps
attainable_TFLOPS = min(compute_roof_TFLOPS, memory_roof_TFLOPS)
```

必须搬运字节数优先按算法最小流量计算，再用 profiler 的实际 HBM/L2 事务解释放大。分别列 read、write、中间张量、重复加载和路由/索引流量。

## 2. 选择正确屋顶

- 物理整卡理论分析：HBM 使用 1843.2 GB/s。
- 当前空闲 sc-16g 工程分析：HBM 使用 1400 GB/s 保守实测屋顶。
- 多租户状态未知：同时报告 460.8、1400、1843.2 GB/s 的敏感性区间，不把 460.8 当已验证硬上限。
- compute roof 按 dtype、MMA 指令、实际时钟和 sGPU 调度选择。若只知道 25% compute quota，可把整卡峰值 ×25% 作为调度模型候选，但必须用 GEMM/microbenchmark 验证。
- mcProfiler 原生图可能使用物理整卡理论屋顶；分析 sGPU 时重新归一化并注明口径。

## 3. 根据瓶颈选择候选

### Memory-bound

- 减少中间张量落 HBM，优先 fusion、in-place 或 producer-consumer 复用。
- 合并连续 load/store，检查 16-byte 或更宽向量化与地址对齐。
- 减少 token/expert 权重的重复加载，利用 shared/register/L2 的真实复用。
- 检查 routing/scatter 导致的非合并访问和过量索引流量。
- 对 8 MiB L2 之外的工作集按 HBM 流量建模，不假设跨大量 expert/sequence 的 cache 常驻。
- 用 `mx-smi --show-hbm-bandwidth` 验证物理带宽，用 profiler 事务量解释为何未达到 STREAM roof。

### Compute-bound

- 先确认生成代码确实使用目标 MMA/MFMA 指令和正确 dtype。
- 提升 M/N/K tile 的 MMA 有效占比，减少边界、mask 和标量尾部。
- 比较默认 emitter 与 manual/private emitter；用生成代码和资源报告验证。
- 调整 `num_stages`、K pipeline、warp/thread layout，并同时监控寄存器、shared memory 和 occupancy。
- 不把较高 occupancy 当目标本身；以延迟和 pipe utilization 为准。

### Latency/grid-bound

- C500 物理上有 104 AP。即使 sGPU `Compute 25%`，当前 runtime 仍枚举 104 AP；不要把 grid 设计成只覆盖 26 AP。
- 计算每个 expert、每个 step 的 block 数和 wave 数。小 M 或 expert 负载不均衡时，增加独立 block、合并 expert 或使用 persistent/fused 路径。
- 评估 launch、同步、routing、scatter/combine 的占比；小 kernel 可能既未触及 compute roof 也未触及 HBM roof。
- 用 mcTracer 分离 step1/step2 及辅助 kernel；不要只看端到端平均。

## 4. MoE 专项检查

1. 按 expert rows 分布计算每个 expert 的 block 数，而不是只看 total tokens。
2. 分别建立 step1 gate/up 与 step2 down 的 FLOPs、字节和时间占比。
3. 检查 padding_M、空 expert、小 expert 尾块和 block 映射浪费。
4. 对 OJ shape 与本地随机分布分别 benchmark；随机 config 不能替代 OJ 性能判断。
5. 优先减少重复读取 routed token、权重和 step1 中间输出；再考虑更激进的 emitter 或 tile。
6. 同一版本同时记录 fusedmoe benchmark、OJ benchmark、mcTracer 分段和 mcProfiler 指标。

## 5. 结论格式

每次硬件感知结论至少回答：

- 使用了哪个机器/切片与哪个 roof？
- 该 roof 是理论、驱动、实测还是保证值？
- 算法 AI 与 ridge point 各是多少？
- 哪个 stage 是主耗时，证据是什么？
- 候选优化改变了 FLOPs、HBM bytes、并行度、资源压力还是 launch 数？
- 哪个实验能证伪当前假设？

