# MAXs VideoEditor

把录屏、直播回放或口播原片做成可直接发布的 9:16 竖屏成片。粗剪、简体字幕、账号包装、图解和渲染由 agent 按流程推进，你只需要在每个检查点确认。

适用两个账号：MAXs 讲游戏美术、技术美术、作品集、升学申请和校招求职；技研Labs 讲 Maya、Blender、3D、模拟与制作流程。

## 快速开始

```bash
npx skills add https://github.com/zzh-editor/MAXs_VideoEditor \
  --skill video-edit --global --agent opencode --copy --yes
```

安装后首次使用前，检查依赖并补齐缺少项：

```bash
SKILL_DIR="$HOME/.agents/skills/video-edit"
test -f "$SKILL_DIR/SKILL.md" || SKILL_DIR="$HOME/.config/opencode/skills/video-edit"
python3 "$SKILL_DIR/scripts/ensure_dependencies.py" --install-missing
```

需要 Node.js 22 或更新版本、FFmpeg，以及渲染用的 Chrome Headless Shell。缺浏览器时运行 `npx hyperframes browser ensure`。

## 开始前准备

把要用的素材放进同一个文件夹：

- 原始录制。有干净无字幕的版本最好，字幕交给技能生成。
- 已有的 SRT。有就直接用，不会重新转写。
- 片头和片尾素材。只用获准使用的，说明画幅和语言。
- 源片的字幕情况。原片已经烧了字幕，说明是保留原字幕，还是另给无字幕原片，不会叠两层。

账号类型、这期讲什么、最想让人记住哪一句，可以在对话里说，也可以等 agent 问。

## 起一条片子

opencode v1 输入 `/`，从列表里选 video-edit，再附上待剪辑视频的文件路径。v2 输入 `@` 选技能，同样附上路径。

然后说清这次的意图，例如：

> 做一条 MAXs 直播切片，围绕「校招比社招更适合应届生」整理成一条完整短片，先粗剪给我看方案，确认后再做字幕和包装，最后要 MP4 和 SRT。

agent 按下面的顺序推进，每个该你决定的点会停下来：

| 阶段 | 你要做的事 |
| --- | --- |
| 粗剪 | 看保留哪些、删哪些、为什么，确认或改。已经人工剪好的直接说，不会重剪 |
| 字幕 | 校对简体字幕。只改文字就指出第几条、改成什么，不用整条重做 |
| 包装 | 确认标题、开口那句话、要不要图解。图解会给字幕出处、时长和画什么 |
| 预览 | 在 HyperFrames Studio 里过一遍，或直接说「渲染」 |
| 交付 | 拿到成片、SRT 和续编说明 |

没说渲染时，agent 停在预览等你；说了就直接渲染，不再追问字幕要不要烧。

## 交付内容

`renders/` 里放三件，主名一致：

| 文件 | 用途 |
| --- | --- |
| `xxx.mp4` | 成片，默认烧录字幕。要一版不带字幕的，说一句即可 |
| `xxx.srt` | 与画面字幕同源的简体字幕，可上传平台，也可当改字幕的底稿 |
| `xxx_续编说明.txt` | 工程在哪、以后怎么改 |

同名文件已存在时，三件一起换成 `xxx_v2`，旧版保留。

## 改片

工程一直是可编辑的，时间线、字幕、图解都能改，渲染不是终点。

- 让 agent 改：把项目文件夹路径和要改的点告诉它。
- 自己在 Studio 里改：在项目文件夹运行 `npx hyperframes preview --background`，打开命令给出的网址，改完保存。
- 刚在 HyperFrames 桌面版改过：先让 agent 运行 `npx hyperframes catch-up`，把应用里的编辑同步回文件，再动文件。

收到第三方反馈时把原文贴进对话，别自己转述：

> 使用 video-edit 继续编辑这个项目：<项目文件夹>
> 第三方反馈：<原文>
> 保留现有剪辑和字幕，只改反馈提到的部分，需要我确认时先停下。

agent 只动相关位置，改完重新渲染会生成新版本，旧文件保留。

## 项目文件

| 位置 | 用途 |
| --- | --- |
| `index.html`、`compositions/` | 时间线、字幕轨、片头片尾、图解 |
| `assets/` | 片尾、音效、字体等素材 |
| `transcript/` | 原始转写、词级时间、成片字幕 |
| `edit-plan.json` | 已确认的保留区间 |
| `BRIEF.md`、`frame.md` | 本条的账号、意图与实际规范 |
| `renders/` | 成片、SRT、续编说明 |

备份或换电脑时复制整个文件夹，只拿 MP4 下次就改不了。

## 账号规范

| MAXs | 技研Labs |
| --- | --- |
| 强调色 `#134FFF`，蓝底白字。蓝色只突出一两个焦点，不加渐变、阴影和装饰图例 | 强调色 `#ADF911` 配黑字。图解段用 `#161616` 全画幅底，不把亮绿铺满屏 |
| 字体 MiSans VF。字幕内强调的词必须来自原字幕 | 字体 MiSans VF。横屏图解底部至少留画面高度 19% 给字幕，竖屏按比例换算 |
| 9:16 图表主体放在 `x=10%–88%`、`y=8%–59%` 的框内，下方留给字幕 | 课程和直播用两行透明片头配 Swoosh，原声从 0 秒开始，片头不增加时长；口播默认不加 |
| 源片烧了福利卡时按实际位置盖住，标题板跟着画面一起移动 | 剪辑不切断操作因果：输入、参数、执行结果和报错留在同一段叙述里 |
| 不默认加品牌片头，开口那句取自口播里的真实主张 | 图解单图单结论，没有真实量值时不硬套成数据图 |

| ![MAXs 校招与社招候选池](skills/video-edit/examples/diagrams/maxs-recruitment-pools.png) | ![技研Labs 父子级变换](skills/video-edit/examples/diagrams/jiyan-parent-child.png) |
| --- | --- |
| MAXs 示例 | 技研Labs 示例 |

SVG 原稿在 [`skills/video-edit/examples/diagrams/`](skills/video-edit/examples/diagrams/)，具体图按当条内容重画，不照搬示例里的数字。

## 常见问题

- 只改一句字幕：说第几条、改成什么。只动文字，不动音频和分段。
- 想换片尾：给出获准的素材，说明画幅和语言。成片不会为了凑尺寸拉伸或裁切落版。
- 要无字幕版：说「要一版不带字幕的」，字幕轨仍留在工程里，SRT 照常给。
- 图解想进 Premiere Pro：先说一声，需要装 Premiere Pro MCP 服务。
- 素材是 4K 或可变帧率：直接给，时间戳按媒体实际时间对齐，输出尺寸和帧率会写进项目文件。

## 致谢

本技能建立在下面这些开源项目之上，它们各自负责一块能力，使用和再分发时请遵守各自仓库的许可：

- [HyperFrames](https://github.com/heygen-com/hyperframes)：把 HTML 组合预览、渲染成视频，Studio 编辑器也由它提供。
- [video-transcribe](https://github.com/zzh-editor/video-transcribe)：转写与字幕流程。
- [Srt-Enhancer](https://github.com/zzh-editor/Srt-Enhancer)：字幕润色。
- [diagram-design](https://github.com/cathrynlavery/diagram-design)：MAXs 图解的图型参考。
- [lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts)：技研Labs 图解的排版参考。
- [pixelfx](https://github.com/patch-gg/pixelfx)：图解的可选素材与特效。
- [Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP)：把图解导入 Premiere Pro。
- MiSans VF 字体由小米提供，片头音效 Swoosh 由技研Labs 提供。
