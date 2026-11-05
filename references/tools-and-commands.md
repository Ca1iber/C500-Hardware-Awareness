# C500 工具与命令

## mx-smi 只读快照

优先运行：

```bash
mx-smi --summary -i 0
mx-smi --show-hwinfo -i 0
mx-smi --show-memory -i 0
mx-smi --show-clock -i 0
mx-smi --show-hbm-bandwidth -i 0
mx-smi --show-ap-usage -i 0
mx-smi sgpu --show-mode -i 0
mx-smi sgpu --show-sched-class -i 0
mx-smi sgpu --show-timeslice -i 0
mx-smi sgpu --show-remain -i 0
```

也可以直接运行 `scripts/collect_c500_snapshot.sh 0`。该脚本已在 sc-16g 的 mx-smi 2.3.1 上验证；不支持的 show 命令会记录 warning 并继续，不执行任何 set/reset 操作。

持续采样物理 HBM：

```bash
timeout 10s mx-smi --show-hbm-bandwidth -i 0 -l 100
```

`--show-hbm-bandwidth` 是物理卡吞吐视图。与 workload 同步采样，排除 idle、启动和阶段切换样本。`sgpu --show-usage` 对毫秒级短 kernel 可能返回 0%，不要单独依赖。

禁止自动执行以下类别：`--reset`、`--kill-all-process`、sGPU `--create/--remove/--set/--enable/--disable`、固件升级、功耗或调度设置。

## HBM STREAM 实验

Skill 中的 `scripts/c500_hbm_stream.cpp` 使用 MXCC 编译：

```bash
/opt/maca/mxgpu_llvm/bin/mxcc -x maca -offload-arch native \
  scripts/c500_hbm_stream.cpp -O3 -o /tmp/c500_hbm_stream \
  --maca-path=/opt/maca
/tmp/c500_hbm_stream
```

PyTorch 交叉验证：

```bash
/opt/conda/bin/python scripts/c500_hbm_torch_crosscheck.py
```

工作集必须远大于 8 MiB L2；记录显式 traffic 口径、warmup、repeat、中位数和 P10/P90。

## mcProfiler

- 先确认 `mcProfiler version` 和实际安装路径。
- 若报缺少 `tilelang-metax/config/.version`，这是工具/项目配置路径问题，不等价于 profiler 二进制不存在。
- 保存原始 JSON、生成图、kernel 名、shape、版本和命令。
- 先核对 `MAX_Bandwith`、compute roof、`MAX_I` 和图中屋顶是否为物理整卡值，再解释百分比。
- 将 profiler 派生带宽与 mx-smi/STREAM 对照，但注明事务统计口径可能不同。

## mcTracer

- 用于确认 kernel 启停顺序、step1/step2 时间、辅助 kernel 和 launch gap。
- 对短 kernel 进行多次稳定采样；避免把首次编译、初始化或 profiler 开销算入 steady state。
- 分段时间占比必须与 benchmark 的端到端口径对齐。

## Roofline 计算

```bash
python3 scripts/roofline_estimator.py \
  --flops 1.0e12 --bytes 8.0e9 \
  --bandwidth-gbps 1400 --compute-tflops 479.232 \
  --time-ms 6.0
```

`compute-tflops` 示例只是模型输入，不是 Skill 对当前 sGPU 的永久保证值。
