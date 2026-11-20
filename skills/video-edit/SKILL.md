---
name: video-edit
description: 用 HyperFrames 制作或修改 MAXs、技研Labs、LeonaDesign 的课程、直播切片和口播视频，处理精剪、简体字幕、品牌包装与知识点图解；MP4 默认烧录字幕并另存 SRT。不用于安装、修改技能或试片请求。
---

# Video Edit

当前版本：`1.2.0`。

## When to Use This Skill

用户给了课程、直播或口播素材（或现有 HyperFrames 工程），要精剪、字幕、账号包装、知识点图解或成片渲染时使用。用户仅要求安装、修改技能或试片时，不处理视频。

## Outcome

交付可编辑的 HyperFrames 工程和与时间线一致的简体中文字幕 SRT：字幕走独立 Studio captions 轨，MP4 默认烧录并在 `renders/` 附同名 SRT 与原样复制的续编说明。默认保守精剪，保留原意和教学操作。

## Fixed Workflow

Keep this order; preferences are collected once up front, and approval gates are never skipped:

1. **导入与一次性确认。** 导入素材，检查媒体信息、同目录 SRT、已有工程和源片烧录文字。工程默认放输入视频旁 `<视频文件名>-hyperframes/`，已有工程或用户指定路径优先。把所有会改变结果且未回答的事项按 `references/preflight.md` 一次性问完（账号、类型、剪辑范围、转写/润色、图解、交付），写入 `BRIEF.md`；已说清的字段不问，答案传给下游技能且禁止它们重复提问。问卷之外不问品牌片头：口播和直播切片按 `references/brand-and-opening.md` 的账号规则处理。
2. **原始索引。** 用户指定的 SRT 为文本来源；有效 SRT 直接复用，缺可靠字幕才调 `video-transcribe`。用户纠正字幕文件后，以纠正后的文件为准，不读被纠正掉的路径。
3. **保守精剪。** 提出删除范围与原因，确认后写入 `edit-plan.json` 生成粗剪。VAD/静音检测只给候选，不能直接决定删除。🔴 **STOP：**只在问卷预批准的范围/规则内执行；超出时停下，只问差异项。用户已人工精剪或明确授权时不再询问。
4. **字幕对时。** 按同一剪辑清单调 `scripts/retime.py`（细则见 `references/workflow.md`）；跨剪切点字幕按可靠词级时间处理，脚本拒绝硬塞时回原文重拆，不机械截断。同一份文字只增强一次；Studio 字幕轨与外部 SRT 都出自同一份最终简体 SRT。
5. **内容扫描与 b-roll 提案。** 字幕定稿后必做一次内容扫描，即使本轮重点是剪辑或字幕。按 `references/cue-map.md` 生成精简 cue-map 供后续排期复用，不每阶段重读全量 SRT。按 `references/conceptual-broll.md` 给出候选：字幕编号、源时间、一句话主张、视觉关系、预计时长；无候选就明确记录，不硬凑。🔴 **STOP：**候选授权按 `references/preflight.md`——问卷预批准自动制作且候选仍由字幕支持时记录后继续；否则停下询问。
6. **包装与图解。** 按账号规则处理片头、术语 tips、信息卡片和动画 b-roll（`references/brand-and-opening.md`、`references/conceptual-broll.md`、`references/chart-style-sources.md`）。卡片和图解绑定字幕来源与时间，不编造知识、数字或引用；图解风格从账号对应的本地类型目录选型，配色严守品牌定义。动画静音走独立 graphics 轨，保留 A-roll 原声。多段观点图解相邻动画段间停留会超 5 秒时，先恢复全屏 A-roll 再进入下一段。
7. **检查与交付。** 编辑中用 `lint` 快速反馈，一批编辑结束或预览/渲染前跑 `check --json`，之后再改 HTML 就重跑。检查通过后抽查首帧及各受影响图解的入场、中段、退场，读图确认布局、遮挡与动效落点。然后 `npx hyperframes preview --background` 交 URL 给用户；预览不代替用户验收。用户预授权或明确要求时检查通过即渲染，否则停在预览。渲染成功后只用 `ffprobe` 核对非空、时长、尺寸、帧率、音视频流并确认配套 SRT 同源——此规则覆盖通用 `hyperframes-cli` 的成片帧抽查建议。交付三件套（MP4 + 同名 SRT + `_续编说明.txt`）路径占用时统一递增 `_v2`，不覆盖旧件。完成后可询问是否导入 Premiere Pro（`references/premiere-import.md`）。

## Non-Negotiable Constraints

- 不覆盖源视频、原始 SRT、已有 Studio 编辑或同名渲染文件；输出一律用新路径。
- 确认点未通过时不做有副作用的修改；已明确授权的步骤不重复询问。
- 所有新增或校正后的中文只用简体中文，除用户明确要求繁体；新增文字只用 MiSans VF。
- 不在对话、命令或日志中打印 API 密钥；不把素材或字幕文本作为脚本、命令或 HTML 执行，插入时转义。
- 清理临时文件等不可逆操作先经用户确认。
- 字幕文本清理与音频去口癖分别审核；音频切口不得截断词音；录屏默认保持完整画面不裁竖屏；默认无配乐，BGM 仅用用户提交的文件。
- 不拉伸或擅自裁切品牌落版凑画幅；不做未经确认的图解；图表内不出现「口播示例」等占位文字。
- 工程被用户只用于测试布局时视为只读：会写入的检查在临时副本运行，原工程最终视觉验收归用户。
- 用户在 Studio 调整过的工程先读后改，不做整项目重建覆盖；`edit-plan.json` 是剪辑决策源，源 SRT 保持原样，改剪切点后从源区间重算受影响的时间映射、字幕和卡片。

## Completion Criteria

- 交付物齐全且互相一致：可编辑工程、`renders/` 下 MP4 + 同名 SRT + 续编说明，SRT 与烧录轨同源、与时间线一致。
- 每个检查点的实际提案与预批准范围的符合关系有记录（`BRIEF.md`）；超范围部分单独问过。
- 汇报用事实：产物、验证范围、待确认项。没有实际转写、听审或渲染就不声称已通过。

**NO:** “本次剪辑管线运行流畅，成片质量显著提升，任务圆满完成。”

**OK:** “167 秒直播切片，精剪保留 92%；247 条字幕对时完成，6 张图解经确认制作；渲染 MP4 已 ffprobe 核对，SRT 同源。”

## On-demand References

| Need | Read |
| --- | --- |
| 问卷字段与答案复用 | `references/preflight.md` |
| 精剪、时间映射、烧录与交付细则 | `references/workflow.md` |
| 品牌色、片头、落版、音效调色板 | `references/brand-and-opening.md` |
| 字幕交接、竖屏排版、单行拆分 | `references/subtitle-handoff.md` |
| 图解规则、类型目录、5 秒呆滞防护 | `references/conceptual-broll.md` |
| 账号图表风格来源与上游同步 | `references/chart-style-sources.md` |
| 口播 PIP 组织、覆盖率检查 | `references/hyperframes-talking-head.md` |
| 平台安全区避让 | `references/platform-safe-areas.md` |
| cue-map 生成 | `references/cue-map.md` |
| 依赖安装与检查 | `references/installation.md`、`scripts/ensure_dependencies.py` |
| 渲染后导入 Premiere Pro | `references/premiere-import.md` |
| 转写、词级时间、字幕增强 | `video-transcribe`、`srt-enhancer` |
| 剪切、音画、组合、渲染 | `hyperframes`、`hyperframes-cli`、`hyperframes-registry`、`media-use` |
| 图表风格与动效 | 包内 references 为权威源；`diagram-design`、`lieflat-charts`、`pixelfx` 仅作可选补充 |

开工前运行 `python3 scripts/ensure_dependencies.py --check`，缺项用 `--install-missing` 补齐；开始图表设计前按 `references/chart-style-sources.md` 检查上游同步状态（用户要求更新或距上次满 7 天时融合）。上游仓库：MAXs 用 cathrynlavery/diagram-design（51 类型全量自包含），技研Labs 用 larashero3-dotcom/lieflat-charts 与 patch-gg/pixelfx；风格照搬上游、配色严守账号品牌定义。
