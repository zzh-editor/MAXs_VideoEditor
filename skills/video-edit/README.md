# MAXs VideoEditor

`video-edit` 是 OpenCode 的 HyperFrames 剪辑 skill，覆盖 MAXs 与技研Labs 的课程、直播和口播切片。它把粗剪决策、简体字幕、账号包装、图解和渲染留在同一套可编辑工程里；视觉预览交给你在 HyperFrames Studio 中检查。

## 安装

需要 Node.js 22+ 和 FFmpeg。安装到 OpenCode 全局 skills 目录：

```bash
npx skills add https://github.com/zzh-editor/MAXs_VideoEditor \
  --skill video-edit --global --agent opencode --copy --yes
```

首次使用前检查依赖，只补缺少项。`skills` CLI 可能把副本放在 `~/.agents/skills/` 或 `~/.config/opencode/skills/`；按安装输出中的实际目录执行：

```bash
SKILL_DIR="$HOME/.agents/skills/video-edit"
test -f "$SKILL_DIR/SKILL.md" || SKILL_DIR="$HOME/.config/opencode/skills/video-edit"
python3 "$SKILL_DIR/scripts/ensure_dependencies.py" --check
python3 "$SKILL_DIR/scripts/ensure_dependencies.py" --install-missing
```

依赖按来源仓库分组安装，清单在 [`skills/video-edit/references/dependencies.json`](skills/video-edit/references/dependencies.json)。HyperFrames 的格式、确定性时间线和工具契约由 `hyperframes` / `hyperframes-cli` 提供；MAXs 动效节奏、A-roll/PIP 组织和图解规则写在本技能的参考文件中。账号色彩、安全框、字幕规范、图解规则和 4 组可编辑 SVG 原稿及对应 PNG 预览都随 `video-edit` 安装；图解以包内规则和 SVG 为准，`diagram-design`、`lieflat-charts`、`pixelfx` 只是可选补充，不会阻塞基础安装。首次安装可能要克隆较大的 HyperFrames 仓库，依赖脚本默认把克隆超时设为 10 分钟。

仓库自带 MiSans VF、技研Labs 固定片头 Swoosh、剪辑/字幕脚本、参考文档、测试和图表示例。渲染需要 Chrome Headless Shell；可运行 `npx hyperframes doctor --json` 检查，缺少浏览器时运行 `npx hyperframes browser ensure`。Premiere Pro、MCP 服务和 Bridge 不在依赖管线内，只在用户要求导入图解且本机已有 MCP 时手动使用，不是基本剪辑和渲染的前置条件。

## 工作顺序

1. **导入并确认需求。** 新工程默认放在导入视频所在目录下的 `<视频文件名>-hyperframes/`；已有工程优先复用。导入后先检查素材和现有字幕，再一次性询问账号、视频类型、字幕选项及本片需要确认的剪辑/图解事项，避免在后续检查点重复提问。
2. **定稿字幕。** 使用词级时间对齐和校对简体字幕。竖屏字幕单行显示，超宽 cue 按语义边界拆分，不靠缩小字号或自动折行。Studio captions 轨与 SRT 必须来自同一份定稿；字幕间距、润色与术语选项在导入问卷中确认。
3. **按账号包装。** 标题、颜色、字体、字幕强调和图解遵循下方账号规范。源片有硬烧录福利卡时，先定位卡片文字区域，再按这条素材实际边界做遮罩；图解节点跟着口播 cue 出现。
4. **检查并交付。** 迭代时用 `lint` 快速反馈；一批修改结束后运行一次 `check --json`，再对首帧和改动时间点抽帧、阅读图像。发现画面问题就修复并复查。随后打开 HyperFrames 桌面应用，留给用户做最终验收。用户已要求或在导入问卷中预先授权渲染时，机器检查和预渲染抽帧通过后直接渲染；否则停在预览交接。MP4 默认烧录字幕；成功后只核对容器信息及同名 SRT、续编说明，不再抽查成片帧。需要时间线信息时筛选 `timeline --json`；涉及图解/PIP 时只生成并复用一份精简 cue map。

完整入口见 [`skills/video-edit/SKILL.md`](skills/video-edit/SKILL.md)，详细规则在 [`skills/video-edit/references/`](skills/video-edit/references/)。

## MAXs

### 视觉规范

- 强调色只有 `#134FFF`；蓝底白字。常规图解用白或纸灰底、黑灰文字、细分隔线，蓝色一般只突出 1–2 个视觉焦点。
- 新增文字使用 MiSans VF。不要用其他账号颜色，不加渐变、阴影、装饰图例，也不为视觉效果虚构数据。
- 9:16 图表主体在 `x=10%–88%`、`y=8%–59%` 的项目框内；下方字幕独立排版。全屏 A-Roll 是口播常态，只有图解需要阅读时才把 A-Roll 与标题板一起缩进下方 PIP，结束后在自然口播边界回全屏。
- 字幕内强调用蓝底白字，词句必须来自原字幕。独立漂浮花字、人物抠像、持续慢推和自动 punch-in 都不是默认包装。
- 标题板会遮住源片烧录的福利卡。每条素材先抽 3–5 帧找出文字边界，不固定假设在左上角；标题板跟 A-Roll 同组移动，PIP 时仍需盖住原卡片。
- MAXs 中文竖版落版也可供技研Labs 共用作片尾；按画幅和语言选获准素材，检查实际尺寸、时长与音轨后接在 A-Roll 后，不从某台机器的固定路径取素材。

### 负责的剪辑方向

MAXs 处理游戏美术、技术美术、作品集、升学申请、校招求职主题的课程/直播切片和口播。剪辑先保留完整论点、操作步骤与必要反应时间，再处理重录和空白；开场 Hook 取自口播中的真实主张。没有明确要求时，不额外加品牌片头。字幕提供信息，图解解释关系，A-Roll 保留说话人和手势。

### 图表示例

招聘路径图只示意口播中的“校招/社招候选池”关系，不代表通用招聘统计；时间线示例的数字也只是示范如何把口播时长关系画出来。

| 校招与社招候选池 | 求职准备时间线 |
|---|---|
| ![MAXs 校招与社招候选池示例](skills/video-edit/examples/diagrams/maxs-recruitment-pools.png) | ![MAXs 求职准备时间线示例](skills/video-edit/examples/diagrams/maxs-study-timeline.png) |

## 技研Labs

### 视觉规范

- 唯一强调色是 `#ADF911`；绿色焦点配黑字。图解活动段使用 `#161616` 全画幅底色，辅以白字、灰字和低对比结构线；不要把亮绿铺成整页背景。
- 新增文字使用 MiSans VF。横屏图解底部留出至少画面高度 19% 的字幕空带；竖屏按高度同比换算。连线、标签、动画行程也要避开这条带。
- 图解优先画真实层级、空间、因果和操作顺序。一个图解只讲一个主关系，节点数量跟着内容走；没有数据时不用统计图，不造指标。
- 课程/直播用固定两行透明片头和 Swoosh，视频、原声从 0 秒连续播放，片头不增加时长；口播默认不加该固定片头。

### 负责的剪辑方向

技研Labs 面向 Maya、Blender、3D、美术技术、模拟和制作流程课程。剪辑不能切断操作因果：输入、参数、执行结果和错误反馈要保留在同一段叙述里。短暂停顿可以缩短，等待渲染时可以压缩，但不能把“怎么设”和“看到什么结果”剪散。

图解只画字幕或课程材料能支撑的技术关系。层级、坐标、管线步骤适合做图；菜单、快捷键和录屏已能说明的内容不再叠一张卡。用线条生长、节点依次出现或状态变化讲顺序，图解节点按口播 cue 推进，不让动画开头几秒播完后空停。

### 图表示例

| Maya 父级与子级 | 模型制作流程 |
|---|---|
| ![技研Labs 父子级变换示例](skills/video-edit/examples/diagrams/jiyan-parent-child.png) | ![技研Labs 模型制作流程示例](skills/video-edit/examples/diagrams/jiyan-model-pipeline.png) |

这些是静态风格示例；SVG 原稿位于 [`skills/video-edit/examples/diagrams/`](skills/video-edit/examples/diagrams/)，视频中的具体图解仍要根据当条素材重画和定时。

## 测试与依赖

在仓库根目录运行：

```bash
python3 -m unittest discover -s skills/video-edit/tests
python3 skills/video-edit/scripts/ensure_dependencies.py --check
```

`lieflat-charts` 是可选参考，使用 PolyForm Noncommercial。本 skill 仅引用其公开视觉原则，不复制其代码、模板和素材；商业发布时需遵守该依赖的许可证。Premiere Pro 服务、MAXs 官方落版素材均不随仓库提供，缺少时按需向使用者索取，不依赖个人电脑绝对路径。

仓库当前未声明整体许可证。MiSans VF 和 Swoosh 是随包的用户提供资产；公开分发或用于其他品牌前，请先确认相应授权。第三方 Agent Skills 由安装脚本从各自上游仓库获取，使用前请审阅其安全与许可证说明。
