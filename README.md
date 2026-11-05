# C500 Hardware Awareness

面向沐曦曦云 C500 的硬件知识技能，用带证据、作用域和复现方法的工程事实，支持 GPU 算子分析与优化。

## 与 C500-OPT 配合

本技能与 [C500-OPT](https://github.com/Ca1iber/C500-OPT) 是两个独立技能：

| 技能 | 职责 |
|---|---|
| `c500-hardware-awareness` | 核验硬件与 sGPU 参数，建立性能模型，维护硬件知识，提出硬件感知优化建议 |
| `c500-opt` | 组织内核优化实验、正确性检查、官方/OJ benchmark、profiling、归档与提交 |

硬件知识按证据规则更新：稳定整卡事实写入 `references/hardware-specs.md`，机器、驱动与调度相关事实写入 `references/sgpu-runtime.md`。新增记录保留证据等级、日期、机器、软件版本、来源和复现方法；存在冲突时解释作用域差异。

两个技能的知识文档需要显式维护与同步；本仓库未实现自动同步或自动发布机制。

## 安装与调用

以下示例使用默认的技能目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Ca1iber/C500-Hardware-Awareness.git ~/.codex/skills/c500-hardware-awareness
```

使用自定义 `CODEX_HOME` 时，将安装位置调整为其下的 `skills/c500-hardware-awareness`。已有同名技能时，先在其他目录检查更新，保留本地修改。

安装后在下一轮对话中调用：

```text
使用 $c500-hardware-awareness，核对当前 C500 实例的硬件与 sGPU 上下文，并建立分阶段 Roofline 模型。
```

与优化技能配合：

```text
同时使用 $c500-opt 和 $c500-hardware-awareness，先确认硬件上下文与测试入口，再根据测量定位瓶颈并优化内核。
```

## 内容

```text
SKILL.md                            技能入口与知识更新规则
agents/openai.yaml                  显示名称与默认调用提示
references/hardware-specs.md        整卡规格、已知事实与待验证参数
references/sgpu-runtime.md          sGPU 配额、调度与测量记录
references/evidence-rules.md        证据等级、必填字段与冲突处理
references/optimization-guide.md    Roofline 与优化候选映射
references/tools-and-commands.md    工具与复现命令
references/sources.md               官方资料及项目实验来源
scripts/                            硬件快照、Roofline 估算与 HBM 测量工具
```

实际硬件查询、编译、benchmark 与 profiling 在目标算力环境执行，遵守项目 `AGENTS.md` 和用户约束。原始实验数据按项目与赛道规则归档，技能文档保存结论及原件引用。

`scripts/c500_hbm_stream.cpp` 和 PyTorch 带宽脚本用于硬件诊断；比赛提交使用 `c500-opt` 定义的源码与计时约束。

详细流程见 [SKILL.md](SKILL.md)。
