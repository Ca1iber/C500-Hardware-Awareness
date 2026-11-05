---
name: c500-hardware-awareness
description: "记录、核验并应用沐曦曦云 C500 的硬件、sGPU、MXMACA 和性能模型事实。Use when Codex needs to answer C500 AP/HBM/L2/clock/compute questions; inspect mx-smi, mcProfiler, or mcTracer results; build or correct a Roofline model; distinguish full-card theory from 16G/25% sGPU behavior; choose TileLang/MXMACA tile, grid, pipeline, layout, fusion, or memory optimizations; or add newly measured C500 parameters with reproducible evidence."
---

# C500 Hardware Awareness

把 C500 参数当作带作用域和证据等级的工程事实使用，并把硬件约束转换成可验证的算子优化决策。

## 核心约束

1. 先确定作用域：物理整卡、`16g`、`sc-16g`、`64g`、特定 sGPU，或特定软件版本。
2. 始终区分四类数值：理论峰值、驱动观测、单租户实测、平台保证值。没有证据时不要把前三者写成保证值。
3. 为参数标注证据等级、日期、机器、软件版本、命令或数据路径。按 [evidence-rules.md](references/evidence-rules.md) 记录。
4. 当前运行状态具有时效性。涉及时钟、sGPU 配额、调度类、可用显存、HBM 吞吐或 GPU mount 时，优先重新查询，不沿用旧会话结果。
5. 不把 `Compute 25%` 推导成所有资源都为 25%。分别验证 AP 可见性、调度、显存容量、HBM、L2 和时钟。
6. 不根据 profiler 图中的单一百分比直接宣布瓶颈。先核对 profiler 使用的屋顶、流量口径、kernel 时间和当前 sGPU 实测屋顶。
7. 未经用户明确授权，只运行 `show/query/help/list` 类命令；不要执行 sGPU create/remove/set、reset、kill、升级或功耗设置。
8. 不在本 Skill、实验报告或脚本中存储 SSH 密码、私钥或临时令牌。

## 工作流

### 1. 建立当前硬件上下文

- 读取 [hardware-specs.md](references/hardware-specs.md) 获取整卡稳定事实。
- 涉及切片或云实例时，再读取 [sgpu-runtime.md](references/sgpu-runtime.md)。
- 需要当前状态时，在目标机运行 `scripts/collect_c500_snapshot.sh [device_id]`。
- 明确输出中的物理卡字段与当前进程可见字段，例如物理 64 GB 与 sGPU 可见约 16 GB。

### 2. 建立性能模型

- 分 kernel 或分 stage 计算 FLOPs、必须搬运字节数和 arithmetic intensity；不要只算整个算子的总量。
- 根据任务选择带宽屋顶：物理理论、当前实例实测或竞争条件下的敏感性区间。
- 根据数据类型和真实指令路径选择 compute roof；不要把 FP16 MMA 峰值用于标量、向量或未走 MMA 的路径。
- 使用 `scripts/roofline_estimator.py` 计算 ridge point、理论上界和实测利用率。
- 按 [optimization-guide.md](references/optimization-guide.md) 把模型转换成 tile/grid/fusion/layout/pipeline 候选。

### 3. 用工具闭环验证

- 用 benchmark 的 device event 或官方计时口径确认延迟。
- 用 mcTracer 分离 step、kernel 与 launch 时间占比。
- 用 mcProfiler 检查访存、计算、cache、资源和 Roofline，但核对其屋顶是否按整卡理论值归一化。
- 用 `mx-smi --show-hbm-bandwidth` 和 `--show-ap-usage` 交叉验证物理吞吐与 AP 分布。
- 保存 warmup/repeat、shape、dtype、git 状态、机器后缀和软件版本。跨 `16g/sc-16g/64g` 不直接混合绝对时间。

### 4. 更新硬件知识

- 先按 [evidence-rules.md](references/evidence-rules.md) 判断证据等级。
- 将稳定整卡事实写入 [hardware-specs.md](references/hardware-specs.md)。
- 将机器、驱动或调度相关事实写入 [sgpu-runtime.md](references/sgpu-runtime.md)。
- 将可复现实验与原始数据按项目 `AGENTS.md` 和 `c500-opt` 的赛道规则归档；在 reference 中只保留结论、原件路径和复现口径。
- 发现冲突时保留两条记录并解释作用域差异；不要静默覆盖旧值。

## Reference 路由

- 整卡 AP、HBM、L2、时钟、功耗和已知/待验证参数： [hardware-specs.md](references/hardware-specs.md)
- `sc-16g` 等 sGPU 配额、调度、实测带宽与版本： [sgpu-runtime.md](references/sgpu-runtime.md)
- Roofline、bound 判断和算子优化映射： [optimization-guide.md](references/optimization-guide.md)
- mx-smi、mcProfiler、mcTracer 和带宽实验命令： [tools-and-commands.md](references/tools-and-commands.md)
- 证据等级、字段模板和更新规则： [evidence-rules.md](references/evidence-rules.md)
- 官方链接与项目实验来源： [sources.md](references/sources.md)

需要内核优化、官方/OJ benchmark、实验归档或提交工作流时，同时使用 [`c500-opt`](https://github.com/Ca1iber/C500-OPT)，遵守其赛道与提交约束；本 Skill 负责硬件事实、性能模型和硬件感知优化建议。需要查阅比赛规则时，可同时参考 `metax-op-competition`。

