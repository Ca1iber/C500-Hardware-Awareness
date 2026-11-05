# C500 参数证据规则

## 证据等级

| 等级 | 含义 | 可用于什么结论 |
|---|---|---|
| `OFFICIAL` | 沐曦产品页、正式手册或官方技术材料明确写出 | 稳定产品规格；仍记录产品/版本范围 |
| `DRIVER` | `mx-smi`、runtime properties、编译器或 profiler 在目标机直接报告 | 当前硬件/软件环境事实 |
| `BENCHMARK` | 可复现实验、原始数据和计时口径支持 | 特定机器与负载下的有效性能 |
| `INFERRED` | 由多个事实和公式推导，但没有直接规格声明 | 性能模型和待验证假设，必须展示公式 |
| `UNKNOWN` | 无公开资料、工具无法查询或实验尚未覆盖 | 明确列为 TODO，不猜测 |

## 必填字段

新增或修改参数时记录：

```text
parameter:
value_and_unit:
scope: full-card | 16g | sc-16g | 64g | sgpu-id
evidence: OFFICIAL | DRIVER | BENCHMARK | INFERRED | UNKNOWN
observed_at:
machine:
software: mx-smi / KMD / MACA / BIOS / TileLang versions
source: URL, command, log, CSV, JSON, or report path
reproduction:
notes:
```

## 冲突处理

1. 先检查单位：GB/s 与 GiB/s、MB 与 MiB、FLOP 与 instruction、单向与双向、读/写与读加写。
2. 再检查作用域：整卡理论、sGPU 可见、物理卡计数器、kernel 派生值、云平台保证值。
3. 再检查时间与版本：时钟、驱动计数器和虚拟化策略可能变化。
4. 保留可解释的多值，例如 `1843.2 GB/s theoretical` 与 `1.43–1.46 TB/s sc-16g idle effective`。
5. 只有新证据真正覆盖相同作用域和口径时才替换旧值；否则并列记录。

## 禁止的推导

- 不由显存容量百分比推出 HBM、L2、PCIe、功耗或时钟百分比。
- 不由 sGPU `Compute` 百分比推出固定 AP 数；必须查看 AP 可见性和运行中分布。
- 不由单次 profiler 百分比推出平台保证带宽。
- 不由峰值样本替代持续中位数。
- 不把 mcProfiler 派生带宽与按显式 load/store 字节计算的 STREAM 带宽视为完全同口径。

