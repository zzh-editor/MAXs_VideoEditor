---
name: video-edit
description: 用 HyperFrames 制作或修改 MAXs、技研Labs、LeonaDesign 的课程、直播切片和口播视频，处理精剪、简体字幕、品牌包装与知识点图解；MP4 默认烧录字幕并另存 SRT。
---

# Video Edit

当前版本：`1.1.2`。

交付可编辑 HyperFrames 项目和与时间线一致的简体中文字幕 SRT。默认保守精剪，保留原意和教学操作；字幕始终放在独立的 Studio 字幕轨，不直接写入源视频。MP4 默认烧录字幕；用户明确要求无字幕时才覆盖默认。每次 MP4 渲染还要在 `renders/` 放同名 SRT 和续编说明。字幕完成后扫描内容；候选图解需用户确认，用户已指定图解内容和字幕区间时直接制作。用户仅要求安装、修改技能或试片时，不处理视频。

## 字幕语言与导出

- 所有新增或校正后的中文只用简体中文，除非用户明确要求繁体。转写优先复用 `video-transcribe` 的简体中文提示；若结果仍有繁体，在现有字幕校对阶段修正文字，保留原始转写和时间轴，不要求安装额外转换依赖。细则见 `references/subtitle-handoff.md`。
- 在 Studio 建一个独立的 `data-track-kind="captions"` 子组合轨道。SRT 是同一份审核字幕的独立文件；不要把字幕做成视频像素或合并进 A-roll。
- MP4 默认把当前可见字幕轨烧录进画面；只有用户明确要求无字幕 MP4 时，才在临时副本中隐藏字幕轨，不能改写用户可编辑的主项目轨道。两种模式都要把同一份审核后的简体 SRT 复制到 `renders/<成片文件名>.srt`。交付与续编说明见 `references/workflow.md`。
- 竖屏字幕按 A-roll / chart-PIP 两种位置模式排版。取消独立漂浮花字；只在无图表的全屏 A-roll 字幕内高亮具体关键词/短语，不整行变色、不加字幕中没有的新词。MAXs 规则见 `references/brand-and-opening.md`，坐标与分段见 `references/subtitle-handoff.md`；发布平台安全区见 `references/platform-safe-areas.md`。
- 屏幕字幕保持单行；超宽 cue 按语义和词级时间拆分，并检查实际字号下的排版。前 30 秒是黄金时间，按 `brand-and-opening.md` 的密度要求安排字幕内强调、音效和第一次画面变化。细则见 `references/subtitle-handoff.md`。
- 图表不加“蓝色表示当前重点”这类装饰色说明；只有真实数据分类需要解释时才放语义图例。
- 图表创作先判断信息关系，再选择图形类型；按账号使用独立视觉规范，规则见 `references/conceptual-broll.md`，品牌色见 `references/brand-and-opening.md`。

## 入口：先账号，再类型

新视频按顺序使用 Question 工具，每次一个问题，等待回答：

1. “这条视频发布到哪个账号？”选项 `MAXs`、`技研`、`LeonaDesign`。`技研` 与 `技研Labs` 归一为 `jiyan`，`MAXs` 为 `maxs`，`LeonaDesign` 为 `leonadesign`。
2. “这是什么类型的视频？”选项 `课程切片`、`直播切片`、`口播视频`，分别记为 `course`、`live`、`talking-head`。

本次用户已经明确给出的字段直接记录，不重复问；新素材不能沿用上一条视频的账号猜测。恢复同一项目或仅调整字幕/卡片时读取项目记录，不重新采访。两个字段就位前不转写、不剪辑、不套片头。例外只有只读的安装和依赖检查。

读 `references/brand-and-opening.md` 决定品牌色与开场。口播和直播切片不询问是否加品牌片头；按账号规则处理。技研课程/直播使用固定片头。内容 Hook 是源视频片段，不等于品牌片头。字体、颜色、音效为用户约束，优先于官方工作流的默认字体配对和配乐建议。

MAXs 包装源视频时抽 3–5 帧定位福利卡文字，再按本条素材重新确定遮罩位置和尺寸；标题板盖住福利卡后放视频标题，并与 A-Roll 同组运动。画幅推拉只在用户要求时添加；用户要求撤销时保留既有 PIP 关键帧和 Studio 编辑。细则见 `references/brand-and-opening.md`。

技研课程/直播的标题是覆盖在视频开头的透明叠加层；视频与 Swoosh 从 0 开始，标题晚 5 个输出帧入场，Swoosh 使用 `data-volume="0.66"`。无独立黑底、无插入时长，`intro_ms: 0`。

## 分工与项目建立

加载 `hyperframes` 了解现行框架路由与时间线契约；上游已将 `general-video` 并入 `hyperframes`，不要求安装独立的 `general-video`。本技能负责领域需求、账号、类型、精剪决策和字幕交接，技术操作使用相应技能的当前契约：

| 工作 | 技能 |
| --- | --- |
| 转写、词级时间、字幕增强 | `video-transcribe`、`srt-enhancer` |
| 素材剪切、音画时间、HTML 组合 | `hyperframes`、`hyperframes-cli` |
| 动效、缩放、组件复用 | `hyperframes`、`hyperframes-registry` |
| 音效增益、预览、渲染 | `media-use`、`hyperframes-cli` |
| 本地素材登记、后续包装规范 | `media-use`、`hyperframes` |
| 图表风格与动效特效 | 包内 `references/chart-style-sources.md` 和 `examples/diagrams/*.svg` 是权威来源；`diagram-design`、`lieflat-charts`、`pixelfx` 仅作可选补充 |
| talking-head 结构与 HyperFrames 时间线规范 | `references/hyperframes-talking-head.md` |
| 渲染后导入 Premiere Pro | `premiere-pro-mcp`、`references/premiere-import.md` |

每条视频独立项目。用 HyperFrames 的 `init` 建立项目，带视频时关闭自动转写，避免重复识别。拿到源片后先检查是否已有人工剪辑；未剪过时先按字幕和语义做保守粗剪，再进入包装。随即写 `BRIEF.md`，记录 `workflow: hyperframes`，以及已确认的账号、类型、素材、画幅、开场方式和编辑范围；不要把已退役的 `general-video` 写成上游 workflow。将本技能的既定管线作为需求传入，官方入口缺什么才补问什么。执行细则见 `references/workflow.md`；安装状态见 `references/installation.md`。

分发包的技能依赖列在 `references/dependencies.json`，图表上游版本列在 `references/style-upstreams.json`。开始工作前运行 `python3 scripts/ensure_dependencies.py --check`；若缺少当前分支所需的 skill，运行 `--install-missing` 后再继续。安装失败时指出缺失项，不假装已调用该 skill。Premiere Pro 服务本身不是 Agent Skill；只在用户选择导入时按 `references/premiere-import.md` 检查并连接。

开始图表或图表特效设计前，按账号读取 `references/chart-style-sources.md`；字幕或构图需避让平台 UI 时读取 `references/platform-safe-areas.md`；talking-head 剪辑读取 `references/hyperframes-talking-head.md`。图表上游日期见 `references/style-upstreams.json`。用户要求更新，或距上次成功检查满 7 天时，先检查并融合相关上游的样式和动效；检查在下一次相关 `video-edit` 调用时执行，不是后台定时任务。

b-roll 默认作为无声、可编辑的 graphics 子组合加入主剪辑项目，另占 Studio 轨道；保留 A-roll 原声和字幕。只有用户明确要独立交付时，才另建 b-roll 项目。

图解段要让 A-roll 与随身标题贴片一起缩放移入右下角 PIP，并在结束时移回全屏；上方图解 + 底部 A-roll 也使用同一套双向关键帧。字幕样式、PIP 坐标、音效和落版按 `brand-and-opening.md` 的「直播切片 / 口播成片基线」写死，不逐条试参数。切片音效按 `brand-and-opening.md` 的「音效调色板」从技能 `assets/audio/sfx/` 选 4 种以上，同一条视频内复用，音量 0.30–0.34 压在人声之下；不为每句口播加声效。操作细则见 `references/hyperframes-talking-head.md` 和 `references/conceptual-broll.md`。

## 六个阶段

1. **原始索引。** 以用户本次指定的字幕/SRT 为文本来源；已有与素材对应的有效 SRT 时直接复用，不必转写。只有缺少可靠字幕时才调用 `video-transcribe`。保留原始字幕、words 和清理记录；所有后续工作副本和对用户展示的中文字幕按 `references/subtitle-handoff.md` 转成简体。用户纠正了字幕文件时，以纠正后的文件为准，不读取或使用被纠正掉的音频路径。
2. **保守精剪。** 提出删除范围与原因，保护教学操作、句内含义和必要停顿。将确认后的保留段写入 `edit-plan.json`，生成粗剪供审核。VAD/静音检测只能给候选，不能直接决定删除。🔴 **STOP：**用户确认粗剪方案前不落实剪切；用户已提供人工精剪版或明确授权直接执行时，不重复询问。
3. **字幕对时。** 使用同一剪辑清单生成视频片段位置和成片字幕，按 `references/workflow.md` 调用 `scripts/retime.py`。跨剪切点的字幕先按可靠词级时间和实际保留语音处理；脚本拒绝把整句文字硬塞进残余时间。按字幕技能管线完成增强和 diff 审核，同一份文字只增强一次。生成 Studio 字幕轨和外部 SRT 时，二者都从同一份最终简体 SRT 生成。
4. **内容扫描与动画 b-roll 提案。** 字幕定稿后必须执行一次内容扫描，即使本轮重点是剪辑或字幕也不能略过。按 `references/conceptual-broll.md` 找出画面本身无法讲清、适合用动画解释的关系或过程，并给出字幕编号、源时间、一句话主张、视觉关系和预计时长。🔴 **STOP：**候选交用户确认后再制作；用户已明确指定图解内容和区间时直接执行，不重复确认。没有合适内容时明确记录“无候选”，不硬凑。
5. **内容包装与动画 b-roll。** 按品牌规则处理片头；只有用户要求时才把源片片段剪成 Hook。术语 tips 和信息卡片绑定字幕来源与时间，不编造知识、数字或引用。用户已确认 b-roll 提案或已明确授权图解内容和字幕区间后，把概念关系做成动画子组合，放在主项目独立 graphics 轨道；按 `references/conceptual-broll.md` 和 `references/chart-style-sources.md` 的关系、账号风格、安全框和动效规则执行。图表特效先按包内规则选择；PixelFX 已安装时再查其 catalog，未安装时使用 HyperFrames 原生动效，不阻塞制作。只有候选能解释知识点且适配 HyperFrames 确定性时间线时才使用。保留 A-roll 原声和字幕时间；动画静音，不用无关素材填时长。所有新增文字只用 MiSans VF，并且中文只用简体。MAXs 直播切片和口播默认在正片后接固定落版，落版时长计入根组合 `data-duration`。
6. **预览交付。** 用 `check` 检查项目；检查开场、转场、剪切接缝、字幕、动画 b-roll、卡片和结尾。每次交付渲染前先打开 HyperFrames Studio 预览供用户编辑并检查。🔴 **STOP：**用户未明确要求渲染时，停在预览等待确认；用户已经要求渲染时，不等待额外的预览或字幕模式确认，检查通过后直接渲染。字幕默认烧录，用户明确要求无字幕时才切换。用 `ffprobe` 核对 MP4 时长/尺寸/音视频流，并抽查成片接缝、字幕和结尾；有差异就修复后重渲染。每个 MP4 都要在 `renders/` 生成同名 SRT 和 `_续编说明.txt`，说明如何归档完整项目、下次通过 agent 处理第三方反馈并重新打开 HyperFrames Studio，格式见 `references/workflow.md`。SRT 或说明文件生成失败时如实报告，不声称交付齐全。渲染完成并验证后，询问是否把动画图解直接导入当前 Premiere Pro 工程；用户确认后按 `references/premiere-import.md` 操作。输出可编辑项目、简体 SRT、MP4 和续编说明；b-roll 对应的字幕区间写入项目记录。

## 修改与恢复

`edit-plan.json` 是剪辑决策源，源文件保持原样。改剪切点会重新生成受影响的时间映射、字幕和卡片；改标题、品牌色、位置或字体大小不触发重新转写。用户在 Studio 调整过的文件先读后改，不能整项目重建覆盖。

用户只允许用现有工程测试布局时，工程视为只读：可检查源码和已有截图；会写入 `.hyperframes` 的 `check`、`snapshot` 等命令改在临时副本运行，不在原项目目录生成测试产物。

字幕文本清理与音频去口癖分别审核；音频切口不得截断词音。录屏默认保持完整画面，不自动裁成竖屏。背景音乐仅用用户提交的文件，默认无配乐；固定片头 Swoosh 属音效。

中文文案、SRT、片头、tips、字幕轨和动画 b-roll 标注统一使用简体中文；除用户明确要求外，不输出繁体字。

完成时简短报告产物、验证范围和待确认项。没有实际转写、听审或渲染就不声称已通过。测试脚本：`python3 -m unittest discover -s <技能目录>/tests`。

## 禁止项

- 不覆盖源视频、原始 SRT、已有 Studio 编辑或同名渲染文件；输出使用新路径。
- 不在粗剪、图解或画幅适配等确认点未通过时继续有副作用的修改；用户已明确授权的步骤不重复询问。
- 不拉伸或擅自裁切品牌落版来凑画幅，也不制作未经确认且用户未明确要求的图解。
