# C500 来源登记

## 官方来源

- C500 产品页：<https://www.metax-tech.com/prod.html?cid=107&id=21>
  - 64 GB 高带宽显存、最小 1% 软切分、350 W 最大功耗。
- 沐曦技术课件：<https://developer.metax-tech.com/forum/media/attachments/39/d1/El1ADiOoQlsq7kyPEIFB1u2IHcoF2nGVICxS6Yi14awRCnfdinB6F8j1R3CRlVk9/ying-ran-2026052.pdf>
  - 同代曦云产品理论 DRAM-L2 约 1843 GB/s、L2 8 MB 等架构材料。课件使用“曦云某款产品”表述，映射到 C500 时要结合驱动/profiler 交叉验证。
- 曦云系列用户指南：<https://developer.metax-tech.com/api/client/document/file/201/preview/?file_type=pdf>
  - mx-smi 与虚拟化工具入口；详细命令另指向单独的 mx-smi 手册。

## 项目实验来源

以下路径相对于 `tilelang-metax` 仓库：

- `race_tests/experiment/v245_c500_sgpu_hbm_bandwidth_sc-16g.md`
- `race_tests/experiment/v245_c500_sgpu_hbm_bandwidth_sc-16g.csv`
- `race_tests/experiment/v245_c500_mxsmi_hbm_samples_sc-16g.csv`
- `race_tests/experiment/v245_c500_hbm_stream_sc-16g.cpp`
- `race_tests/experiment/v245_c500_hbm_torch_crosscheck_sc-16g.py`

## 更新要求

- 外部资料可能更新；引用精确规格前重新打开原页面或文档。
- 机器运行数据必须重新采集并记录日期与版本。
- 将未经复现的论坛用户数据视为线索，不升级为 `OFFICIAL` 或本机 `DRIVER` 事实。

