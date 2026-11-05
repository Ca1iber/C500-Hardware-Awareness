# C500 整卡硬件事实

更新时间：2026-08-10

## 已确认参数

| 参数 | 当前值 | 证据 | 作用域与备注 |
|---|---:|---|---|
| 产品 | 曦云 C500，PCIe 板卡 | `OFFICIAL` | C500 产品页 |
| 物理显存 | 64 GB | `OFFICIAL` + `DRIVER` | 产品页；`mx-smi --show-hwinfo` |
| 显存类型 | HBM2e | `DRIVER` | `mx-smi --show-hwinfo` |
| 最大板卡功耗 | 350 W | `OFFICIAL` + `DRIVER` | 产品页；`mx-smi` summary |
| 物理 AP 数 | 104 | `DRIVER` | runtime `multi_processor_count=104`；AP 表为 8 DPC × 13 AP |
| L2 | 8 MiB | `DRIVER` | PyTorch runtime properties；官方技术课件中的同代曦云产品相符 |
| MC 时钟观测 | 1800 MHz | `DRIVER` | `mx-smi --show-clock`；时钟属于运行状态，不当作永恒常量 |
| 理论 DRAM-L2 带宽 | 1843.2 GB/s | `DRIVER` + 官方材料佐证 | C500 mcProfiler `MAX_Bandwith`；官方技术课件给同代曦云产品约 1843 GB/s |
| 软切分粒度 | 最小 1% | `OFFICIAL` | 产品页只说明粒度，不说明所有资源按相同比例硬切 |

## 性能模型中的工作值

以下数值可用于建立模型，但必须带证据说明：

| 参数 | 工作值 | 等级 | 说明 |
|---|---:|---|---|
| 物理整卡 HBM Roofline | 1843.2 GB/s | `DRIVER` | 理论屋顶，不是应用持续带宽 |
| C500 原生 Roofline FP16 MMA roof | 1916.928 TFLOP/s | `INFERRED` | 由一次 mcProfiler 模型的 104 AP、1.125 GHz 与每 AP MMA 吞吐重建；使用前重新核对 profiler JSON/图 |
| 对应整卡 ridge point | 1040 FLOP/B | `INFERRED` | `1916.928×1000/1843.2` |

FP16 MMA roof 不适用于未走 MMA 的指令路径。XCORE 时钟会随 DPM、功耗和负载变化；若使用该 roof 做精确结论，必须记录当前 profile 的时钟和生成指令。

## 仍未知或不应硬编码

- L1D/VL1 的可用容量、关联度、替换策略及其对不同访问模式的有效行为。
- Shared memory 每 AP 的精确可用上限与 bank 细节在当前 TileLang/MXMACA 版本下的约束。
- 寄存器文件总量、每线程/每 CTA 分配粒度和 occupancy 公式的完整公开规格。
- 不同 dtype 和不同 MFMA/MMA 指令的权威整卡峰值。
- HBM 在多 sGPU 并发下的 QoS、最低保证和仲裁规则。
- PCIe/MetaXLink 的当前实例有效带宽与拓扑。

遇到这些问题时优先做 microbenchmark、资源编译报告和 profiler 交叉验证，不做 CUDA/NVIDIA 参数的机械类比。

