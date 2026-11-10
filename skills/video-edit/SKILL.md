---
name: video-edit
description: 用 HyperFrames 制作或修改 MAXs、技研Labs、LeonaDesign 的课程、直播切片和口播视频，处理精剪、简体字幕、品牌包装与知识点图解；MP4 默认烧录字幕并另存 SRT。
---

# Video Edit

当前版本：`1.1.8`。

交付可编辑 HyperFrames 项目和与时间线一致的简体中文字幕 SRT。默认保守精剪，保留原意和教学操作；字幕始终放在独立的 Studio 字幕轨，不直接写入源视频。MP4 默认烧录字幕；用户明确要求无字幕时才覆盖默认。渲染时把固定的 `assets/continuation-note.txt` 原样复制到 `renders/`，不按项目重写说明。字幕完成后扫描内容；图解按导入后预确认的策略处理。用户仅要求安装、修改技能或试片时，不处理视频。

## 字幕语言与导出

- 所有新增或校正后的中文只用简体中文，除非用户明确要求繁体。转写优先复用 `video-transcribe` 的简体中文提示；若结果仍有繁体，在现有字幕校对阶段修正文字，保留原始转写和时间轴，不要求安装额外转换依赖。细则见 `references/subtitle-handoff.md`。
- 在 Studio 建一个独立的 `data-track-kind="captions"` 子组合轨道。SRT 是同一份审核字幕的独立文件；不要把字幕做成视频像素或合并进 A-roll。
- MP4 默认把当前可见字幕轨烧录进画面；只有用户明确要求无字幕 MP4 时，才在临时副本中隐藏字幕轨，不能改写用户可编辑的主项目轨道。两种模式都要把同一份审核后的简体 SRT 复制到 `renders/<成片文件名>.srt`。交付与续编说明见 `references/workflow.md`。
- 竖屏字幕按 A-roll / chart-PIP 两种位置模式排版。取消独立漂浮花字；只在无图表的全屏 A-roll 字幕内高亮具体关键词/短语，不整行变色、不加字幕中没有的新词。MAXs 规则见 `references/brand-and-opening.md`，坐标与分段见 `references/subtitle-handoff.md`；发布平台安全区见 `references/platform-safe-areas.md`。
- 屏幕字幕保持单行；超宽 cue 按语义和词级时间拆分，并检查实际字号下的排版。前 30 秒是黄金时间，这套注意力策略可按内容延伸到全片；字幕能支撑图表时优先图表，不适合图表的段落再做有信息量的大字报。细则见 `references/brand-and-opening.md` 和 `references/subtitle-handoff.md`。
- 图表不加“蓝色表示当前重点”这类装饰色说明；只有真实数据分类需要解释时才放语义图例。
- 图表创作先判断信息关系，再选择图形类型；内容应有效铺排安全框，不留大块无意义空白，动效按字幕 cue 分步推进。图解和口播动效必须同时遵循本技能的 `references/chart-style-sources.md`、`references/hyperframes-talking-head.md` 与 `hyperframes` 的 seek-safe 时间线契约；图表规则按需读取 `references/conceptual-broll.md`，品牌色见 `references/brand-and-opening.md`。
- 口播全屏 A-roll 是常态，PIP 只在图解确实需要讲解时使用；独立图解之间在自然停顿、反应或转题处恢复全屏，不把多段图解串成一整段右下角小窗。删除冗余大字报后保留全屏口播，不自动补另一张卡。渲染前按 `references/hyperframes-talking-head.md` 核对 PIP 覆盖率和最长连续区间。

## 新项目：导入后一次性确认

先导入用户给的视频或现有工程，检查媒体信息、同目录 SRT、项目文件和源片已烧录的文字。新建 HyperFrames 工程默认放在输入视频所在目录下的 `<视频文件名>-hyperframes/`；若用户给了工程路径或该目录已是可编辑工程，就使用现有路径，不另建副本。只有默认目录不可写或与其他工程冲突时才询问位置。细则见 `references/workflow.md`。

导入后、开始精剪或包装前，把本项目所有尚未回答且会改变结果的事项汇总成一批问题，通过当前 host 的阻塞式问题机制一次提交；支持多问题列表时用一个调用，不支持时在同一条消息里发一份编号问卷并只等一次回答。不要把账号、类型、字幕选项拆成多轮对话。问卷按本项目实际需要裁剪，用户已经说清的字段不问：

- 账号风格：`MAXs`、`技研Labs`、`LeonaDesign`；`技研` 归一为 `技研Labs`。
- 视频类型：课程切片、直播切片、口播视频。
- 剪辑范围：默认保留用户已剪好的源片；只有拟剪范围会改变内容时才列出范围供选择。
- 若需要转写或润色：转写引擎（仅在没有可用配置时）、是否润色、混排中英空格开关、领域自动识别或手动指定、术语括注开关，以及仅接受不改原意的文字修正还是逐条审 diff。简体中文是默认，翻译须明确要求。
- 图解：按字幕提出的候选自动制作、只列候选不制作，或不加图解。只有用户选择自动制作时，后续图解确认点才算预批准；新候选超出字幕依据时仍需单独询问。
- 交付：用户没有明确要求 MP4 时，选择停在 Studio 预览或在机器检查通过后渲染。

把答案逐项写入 `BRIEF.md`。保留后续精剪、字幕、图解和交付检查点；到达检查点时，如果提案仍在预批准的范围内，就记录为已通过并继续，不重复提问。实际候选或字幕 diff 与预批准范围不符时，只询问变化部分。调 `video-transcribe` / `srt-enhancer` 时传入这些明确答案，禁止它们再问同一事项；它们各自的转写、增强、对时和验证步骤照常执行。完整问卷与复用规则见 `references/preflight.md`。

读 `references/brand-and-opening.md` 决定品牌色与开场。口播和直播切片不询问是否加品牌片头；按账号规则处理。技研课程/直播使用固定片头。内容 Hook 是源视频片段，不等于品牌片头。字体、颜色、音效为用户约束，优先于官方工作流的默认字体配对和配乐建议。

MAXs 包装源视频时抽 3–5 帧定位福利卡文字，再按本条素材重新确定遮罩位置和尺寸；标题板盖住福利卡后放视频标题，并与 A-Roll 同组运动。画幅推拉只在用户要求时添加；用户要求撤销时保留既有 PIP 关键帧和 Studio 编辑。细则见 `references/brand-and-opening.md`。

技研课程/直播的标题是覆盖在视频开头的透明叠加层；视频与 Swoosh 从 0 开始，标题晚 5 个输出帧入场，Swoosh 使用 `data-volume="0.66"`。无独立黑底、无插入时长，`intro_ms: 0`。

## 分工与项目建立

加载 `hyperframes` 了解现行框架路由与时间线契约；上游已将 `general-video` 并入 `hyperframes`，不要求安装独立的 `general-video`。本技能负责领域需求、账号、类型、精剪决策和字幕交接，技术操作使用相应技能的当前契约：

| 工作 | 技能 |
| --- | --- |
| 转写、词级时间、字幕增强 | `video-transcribe`、`srt-enhancer` |
| 素材剪切、音画时间、HTML 组合 | `hyperframes`、`hyperframes-cli` |
| 动效、缩放、组件复用 | `hyperframes`、`hyperframes-registry`、`references/hyperframes-talking-head.md`、`references/chart-style-sources.md` |
| 音效增益、预览、渲染 | `media-use`、`hyperframes-cli` |
| 本地素材登记、后续包装规范 | `media-use`、`hyperframes` |
| 图表风格与动效特效 | 包内 `references/chart-style-sources.md` 和 `examples/diagrams/*.svg` 是权威来源；`diagram-design`、`lieflat-charts`、`pixelfx` 仅作可选补充 |
| talking-head 结构与 HyperFrames 时间线规范 | `references/hyperframes-talking-head.md` |

每条视频独立项目。HyperFrames 工程默认放在输入视频所在目录下的 `<视频文件名>-hyperframes/`；已有工程或用户指定路径优先。用 `init` 时关闭自动转写，避免重复识别。检查是否已有人工剪辑；未剪过时先按字幕和语义提出保守剪辑候选。导入后完成一次性问卷后再进入下游步骤，随后将答案写入 `BRIEF.md`；不要把已退役的 `general-video` 写成上游 workflow。执行细则见 `references/workflow.md` 和 `references/preflight.md`；安装状态见 `references/installation.md`。

已有工程需要核对时间线时，按需运行 `npx hyperframes timeline --json`，仅在命令侧筛选目标时间段和相关 clip 的 `id`、`absStart`、`absEnd`、`file`、`trackKind`；不要把完整 JSON 输出送进上下文。若用户已给出确切 clip ID 与时间段，不重复索引无关轨道。

分发包的技能依赖列在 `references/dependencies.json`，图表上游版本列在 `references/style-upstreams.json`。开始工作前运行 `python3 scripts/ensure_dependencies.py --check`；若缺少当前分支所需的 skill，运行 `--install-missing` 后再继续。安装失败时指出缺失项，不假装已调用该 skill。Premiere Pro 导入不在依赖管线内：`--check` 和 `--install-missing` 都不处理它；只有用户明确要求导入且本机已有 MCP 时，才按 `references/premiere-import.md` 手动执行。

开始图表或图表特效设计前，按账号读取 `references/chart-style-sources.md`；字幕或构图需避让平台 UI 时读取 `references/platform-safe-areas.md`；talking-head 剪辑读取 `references/hyperframes-talking-head.md`。图表上游日期见 `references/style-upstreams.json`。用户要求更新，或距上次成功检查满 7 天时，先检查并融合相关上游的样式和动效；检查在下一次相关 `video-edit` 调用时执行，不是后台定时任务。

b-roll 默认作为无声、可编辑的 graphics 子组合加入主剪辑项目，另占 Studio 轨道；保留 A-roll 原声和字幕。只有用户明确要独立交付时，才另建 b-roll 项目。

需要图解与口播同屏时，让 A-roll 与随身标题贴片一起缩放移入右下角 PIP，并在图解结束时移回全屏；上方图解 + 底部 A-roll 也使用同一套双向关键帧。只在图解需要被读懂的时段维持 PIP，不把它当作口播默认布局。动效按 cue 选择少量能表达关系的动作，统一走确定性、可 seek 的暂停时间线，不加装饰性循环。字幕样式、PIP 坐标、音效和落版按 `brand-and-opening.md` 的「直播切片 / 口播成片基线」写死，不逐条试参数。切片音效按「音效调色板」从技能 `assets/audio/sfx/` 选 4 种以上，同一条视频内复用，并按单个素材的响度配置增益；不为每句口播加声效。细则见 `references/hyperframes-talking-head.md`、`references/chart-style-sources.md` 和 `references/conceptual-broll.md`。

## 六个阶段

1. **原始索引。** 以用户本次指定的字幕/SRT 为文本来源；已有与素材对应的有效 SRT 时直接复用，不必转写。只有缺少可靠字幕时才调用 `video-transcribe`。保留原始字幕、words 和清理记录；所有后续工作副本和对用户展示的中文字幕按 `references/subtitle-handoff.md` 转成简体。用户纠正了字幕文件时，以纠正后的文件为准，不读取或使用被纠正掉的音频路径。
2. **保守精剪。** 提出删除范围与原因，保护教学操作、句内含义和必要停顿。将确认后的保留段写入 `edit-plan.json`，生成粗剪供审核。VAD/静音检测只能给候选，不能直接决定删除。🔴 **STOP：**只在导入问卷明确预批准的剪辑范围/规则内执行；未覆盖或超出范围时停下，只询问差异项。用户已提供人工精剪版或明确授权直接执行时，不重复询问。
3. **字幕对时。** 使用同一剪辑清单生成视频片段位置和成片字幕，按 `references/workflow.md` 调用 `scripts/retime.py`。跨剪切点的字幕先按可靠词级时间和实际保留语音处理；脚本拒绝把整句文字硬塞进残余时间。按字幕技能管线完成增强和 diff 审核，同一份文字只增强一次。生成 Studio 字幕轨和外部 SRT 时，二者都从同一份最终简体 SRT 生成。
4. **内容扫描与动画 b-roll 提案。** 字幕定稿后必须执行一次内容扫描，即使本轮重点是剪辑或字幕也不能略过。若项目会安排图解、卡片、PIP 或 cue 定时音效，按 `references/cue-map.md` 一次生成精简 `transcript/cue-map.md`，后续排期与检查复用；不要每个阶段重读或重印全量 SRT。按 `references/conceptual-broll.md` 找出画面本身无法讲清、适合用动画解释的关系或过程，并给出字幕编号、源时间、一句话主张、视觉关系和预计时长。🔴 **STOP：**按 `references/preflight.md` 处理候选授权：在导入问卷中已批准自动制作且候选仍由字幕支持时，记录预批准并继续；选择只列候选、未回答或候选超出批准范围时停下询问。没有合适内容时明确记录“无候选”，不硬凑。
5. **内容包装与动画 b-roll。** 按品牌规则处理片头；只有用户要求时才把源片片段剪成 Hook。术语 tips 和信息卡片绑定字幕来源与时间，不编造知识、数字或引用。用户已确认 b-roll 提案或已明确授权图解内容和字幕区间后，把概念关系做成动画子组合，放在主项目独立 graphics 轨道；按 `references/conceptual-broll.md` 和 `references/chart-style-sources.md` 的关系、账号风格、安全框和动效规则执行。图表特效先按包内规则选择；PixelFX 已安装时再查其 catalog，未安装时使用 HyperFrames 原生动效，不阻塞制作。只有候选能解释知识点且适配 HyperFrames 确定性时间线时才使用。保留 A-roll 原声和字幕时间；动画静音，不用无关素材填时长。所有新增文字只用 MiSans VF，并且中文只用简体。MAXs 直播切片和口播默认在正片后接固定落版，落版时长计入根组合 `data-duration`。
6. **检查与交付。** HTML 迭代中用 `lint` 快速反馈；一批编辑结束后，在预览、渲染或交接前运行一次 `check --json`。此后若再改 HTML，重跑完整 check。检查通过后抽查首帧，以及每个受影响图解的入场、中段和退场，阅读图像检查布局、遮挡、动效落点、全屏 A-roll 节奏与首尾状态。发现问题就修改、重跑 check 并重新抽帧。然后启动 `npx hyperframes preview --background` 并把 URL 交给用户；预渲染抽帧不代替用户最终验收。若用户明确要求渲染或在导入问卷中预授权渲染，检查通过且预渲染抽帧完成后直接渲染；否则停在预览交接。字幕默认烧录，用户明确要求无字幕时才切换。渲染成功后只用 `ffprobe` 核对文件非空、时长、尺寸、帧率和音视频流，并确认配套 SRT 与最终字幕源一致；不再运行 `snapshot --against`、抽取或检查成片帧。此规则是 `video-edit` 的渲染后检查策略，覆盖通用 `hyperframes-cli` 的成片帧抽查建议。把 `assets/continuation-note.txt` 原样复制为 `renders/<basename>_续编说明.txt`，与 MP4 和同名 SRT 共用一个可用主名；固定文本说明见 `references/workflow.md`。若交付文件路径已占用，统一递增 `_v2` 等主名，不覆盖旧件。完成渲染后仍可询问是否把图解导入 Premiere Pro；用户确认后按 `references/premiere-import.md` 操作。

## 修改与恢复

`edit-plan.json` 是剪辑决策源，源文件保持原样。改剪切点会重新生成受影响的时间映射、字幕和卡片；改标题、品牌色、位置或字体大小不触发重新转写。用户在 Studio 调整过的文件先读后改，不能整项目重建覆盖。

用户只允许用现有工程测试布局时，工程视为只读：可检查源码和已有截图；会写入 `.hyperframes` 的 `check` 或 `snapshot` 改在临时副本运行，不在原项目目录生成测试产物。原工程的最终视觉验收仍由用户在 HyperFrames Studio 完成。

字幕文本清理与音频去口癖分别审核；音频切口不得截断词音。录屏默认保持完整画面，不自动裁成竖屏。背景音乐仅用用户提交的文件，默认无配乐；固定片头 Swoosh 属音效。

中文文案、SRT、片头、tips、字幕轨和动画 b-roll 标注统一使用简体中文；除用户明确要求外，不输出繁体字。

完成时简短报告产物、验证范围和待确认项。没有实际转写、听审或渲染就不声称已通过。测试脚本：`python3 -m unittest discover -s <技能目录>/tests`。

## 禁止项

- 不覆盖源视频、原始 SRT、已有 Studio 编辑或同名渲染文件；输出使用新路径。
- 不在粗剪、图解或画幅适配等确认点未通过时继续有副作用的修改；用户已明确授权的步骤不重复询问。
- 不拉伸或擅自裁切品牌落版来凑画幅，也不制作未经确认且用户未明确要求的图解。

## 管线效率、图表一致性与 Token 优化规则（Fast-Path）

- **References 按需懒加载**：根据 `BRIEF.md` 的账号与导出模式按需读取 `references/`，不导出 Premiere 时不加载 `references/premiere-import.md`。
- **词级重映射与候选窗口聚合**：使用 `python3 scripts/retime.py edit-plan.json source.srt --words words.json --allow-boundary-clip --output-dir dist/` 消除切口报错，并使用 `python3 scripts/pipeline_opt.py extract-cues` 生成 15–25 秒高密度候选窗口，免除全量 SRT 上下文读取。
- **声明式图表与合规校验**：使用 `python3 scripts/pipeline_opt.py render-chart` 结合账号配色 Token 与词级 `step_triggers` 生成动效图表；渲染后调用 `python3 scripts/pipeline_opt.py validate-svg` 检查 viewBox、品牌主色和最小字号（正文 ≥28px）。4px 网格与 9:16 Diagram Safe Box（`x: 108..950, y: 154..1133`，渲染器已按此画框）目前靠 `snapshot` 抽帧目检，脚本不做几何校验。
