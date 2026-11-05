# C500 sGPU 与机器运行事实

更新时间：2026-08-10

## sc-16g 当前快照

| 参数 | 值 | 证据 |
|---|---:|---|
| 设备 | MetaX C500 | `DRIVER` |
| mx-smi | 2.3.1 | `DRIVER` |
| KMD | 3.8.30 | `DRIVER` |
| MACA | 3.7.1.5 | `DRIVER` |
| BIOS | 1.33.5.0 | `DRIVER` |
| sGPU | minor 003, sGPU id 1 | `DRIVER` |
| Compute quota | 25% | `DRIVER` |
| VRAM quota | 16000 MiB | `DRIVER` |
| runtime 可见显存 | 16,341,008,384 bytes，约 15.22 GiB | `DRIVER` |
| runtime 可见 AP | 104 | `DRIVER` |
| 调度类 | best effort | `DRIVER` |
| 时间片 | 10 ms | `DRIVER` |
| 整卡剩余 compute quota | 0% | `DRIVER` |
| 整卡剩余 vram quota | 581 MB / 64,581 MB | `DRIVER` |

同次空闲快照还观测到：XCORE 428 MHz、MC0/MC1 DFI 1800 MHz、SOC/DNOC 1200 MHz、CCX 535 MHz、hotspot 35°C、整卡约 58.4 W。除 MC 的稳定 DPM 档外，这些值属于空闲动态状态，不能直接作为负载时 compute roof。

`Compute 25%` 是调度配额，不是固定暴露 26 AP：streaming 运行中 104/104 AP 都有约 76%～77% 活跃度。当前证据与跨整卡 AP 的时间片调度一致。

不要仅根据 `best effort` 名称声称最低保证、借用上限或公平性规则。当前公开资料与 `mx-smi --help` 没有解释三种调度类的完整语义。

## sc-16g HBM 实验

条件：物理卡无其他进程、工作集 1～2 GiB、L2 为 8 MiB、warmup 10、repeat 31。

| 测量 | 结果 | 解释 |
|---|---:|---|
| MXCC copy，2 GiB | 1440.5 GB/s | 一读一写，两个独立 run 的均值 |
| MXCC triad，2 GiB | 1428.7 GB/s | 两读一写 |
| PyTorch `copy_`，2 GiB | 1424.5 GB/s | 独立实现交叉验证 |
| PyTorch `add(out=)`，2 GiB | 1464.5 GB/s | 两读一写交叉验证 |
| mx-smi 活跃采样中位数 | 1411.5 GB/s | 物理卡驱动计数器，100 ms 采样 |
| mx-smi 活跃采样峰值 | 1507.6 GB/s | 不是持续保证值 |
| MXCC write，2 GiB | 1584.4 GB/s | 单写模式，不作为混合读写默认 roof |

结论：空闲单租户条件下，sc-16g 可获得约 1.43～1.46 TB/s 混合读写有效带宽，远高于把整卡带宽机械乘 25% 得到的 460.8 GB/s。为当前算子 Roofline 使用 1.4 TB/s 作为保守实测带宽；同时保留 1.8432 TB/s 物理理论屋顶。

该结论不是平台保证。其他 sGPU 同时访问 HBM 时可能显著下降；多租户竞争实验仍为 TODO。

## 机器使用规则

- 始终区分 `16g` 与 `sc-16g`，结果文件分别带 `_16g`、`_sc-16g`。
- `64g` 是否为未切片整卡必须通过当次 `mx-smi`/runtime 快照确认，不能只按实例名称推断。
- 跨机器比较必须记录 shape、dtype、warmup/repeat、KMD、MACA、BIOS、TileLang git state 和 GPU mount。
- `mx-smi` 能看到物理 64 GB，而进程 runtime 只看到 sGPU 配额，这是正常的物理视图与进程视图差异。
