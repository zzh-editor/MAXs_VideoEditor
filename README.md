# MAXs VideoEditor

在 opencode 里用一段话起一条片子，agent 负责粗剪、字幕、账号包装、图解和渲染，你负责确认。交付的是可发布的竖屏成片，加一套随时能改的工程。

## 适合剪什么

- MAXs：游戏美术、技术美术、作品集、升学申请、校招求职的直播切片和口播。
- 技研Labs：Maya、Blender、3D、模拟与制作流程课程切片。
- 默认 9:16 竖屏，两个账号各有一套包装和字幕规则。

## 开始前准备

1. 装好 opencode 和本技能，方法见文末「安装」。
2. 素材放进一个空文件夹：原始录制（有干净无字幕版最好）、已有 SRT（有就直接用，不必重新转写）、获准的片头片尾素材。
3. 想清楚三件事：哪个账号、什么类型（直播切片 / 口播 / 课程切片）、这条片子最想让人记住哪一句。

## 起一条片子

在 opencode 里新开对话，把素材位置和意图说清楚，例如：

> 用 video-edit 做一条 MAXs 直播切片，素材在 <文件夹>。围绕「校招比社招更适合应届生」整理成一条完整短片，先粗剪给我看方案，确认后再做字幕和包装，最后要 MP4 和 SRT。

接下来 agent 按顺序推进，每到一个该你决定的点会停下来：

| 阶段 | 你要做的事 |
| --- | --- |
| 粗剪 | 看保留哪些、删哪些、为什么，确认或改。已经人工剪好的直接说，不会重剪 |
| 字幕 | 校对简体字幕。只改文字就指出第几条、改成什么，不用整条重做 |
| 包装 | 确认标题、开口那句话、要不要图解。图解会给字幕出处、时长和画什么 |
| 预览 | 在 HyperFrames Studio 里过一遍，或直接说「渲染」 |
| 交付 | 拿走成片、SRT 和续编说明 |

没说渲染时，agent 停在预览等你；说了就直接渲染，不再追问字幕要不要烧。

## 完成后拿到什么

`renders/` 里三件，主名一致：

- `xxx.mp4`：成片，默认烧录字幕。要一版不带字幕的，明确说一句即可。
- `xxx.srt`：与画面字幕同源的简体字幕，可上传平台，也可当改字幕的底稿。
- `xxx_续编说明.txt`：怎么保存工程、以后怎么继续改。

同名文件已存在时，三件一起换新名字（`xxx_v2`），旧版不会被覆盖。

## 改片子：回到 HyperFrames Studio

工程是活的，时间线、字幕、图解都能改，渲染不是终点。

- 让 opencode 改：把项目文件夹路径和要改的点告诉 agent。
- 自己在 Studio 里改：进项目文件夹运行 `npx hyperframes preview --background`，再运行 `npx hyperframes preview --status` 确认服务起来，打开命令给出的 Studio 地址。改完保存。
- 刚在 HyperFrames 桌面版里改过：先让 agent 运行 `npx hyperframes catch-up`，把应用里的编辑同步回文件，再让 agent 动文件，避免覆盖刚做的修改。

## 收到反馈怎么改

把反馈原文贴进对话，别自己转述：

> 使用 video-edit 继续编辑这个项目：<项目文件夹>
> 第三方反馈：<原文>
> 保留现有剪辑和字幕，只改反馈提到的部分，需要我确认时先停下。

agent 只动相关位置，改完重新渲染会生成新版本，旧文件保留。

## 项目文件夹里有什么

| 位置 | 用途 |
| --- | --- |
| `index.html`、`compositions/` | 时间线、字幕轨、片头片尾、图解 |
| `assets/` | 片尾、音效、字体等素材 |
| `transcript/` | 原始转写、词级时间、成片字幕 |
| `edit-plan.json` | 已确认的保留区间 |
| `BRIEF.md`、`frame.md` | 本条片子的账号、意图与实际规范 |
| `renders/` | 成片、SRT、续编说明 |

备份或换电脑时复制整个文件夹，别只拿 MP4，否则下次改不了。

## 账号规范速查

### MAXs

- 强调色 `#134FFF`，蓝底白字；其余用白或纸灰底、黑灰字。蓝色只突出一两个焦点，不加渐变、阴影和装饰图例。
- 字体 MiSans VF。字幕内强调的词必须来自原字幕。
- 9:16 图表主体放在 `x=10%–88%`、`y=8%–59%` 的框内，下方留给字幕。
- 源片烧了福利卡时，按这条素材的实际位置盖住，标题板跟着画面一起移动。
- 不默认加品牌片头；开口那句话取自口播里的真实主张。

### 技研Labs

- 强调色 `#ADF911` 配黑字；图解段用 `#161616` 全画幅底，辅白字和灰字，不把亮绿铺满屏。
- 字体 MiSans VF。横屏图解底部至少留画面高度 19% 给字幕，竖屏按比例换算。
- 课程和直播用固定两行透明片头配 Swoosh，视频原声从 0 秒开始，片头不增加时长；口播默认不加该片头。
- 剪辑不切断操作因果：输入、参数、执行结果和报错留在同一段叙述里。

### 图表示例

![MAXs 校招与社招候选池](skills/video-edit/examples/diagrams/maxs-recruitment-pools.png)

![技研Labs 父子级变换](skills/video-edit/examples/diagrams/jiyan-parent-child.png)

SVG 原稿在 [`skills/video-edit/examples/diagrams/`](skills/video-edit/examples/diagrams/)，是图解的样式依据；具体图仍按当条内容重画，不照搬示例里的数字。

## 常见问题

- 只改一句字幕：说第几条、改成什么。只动文字，不动音频和分段。
- 想换片尾：给出获准的素材，说明画幅和语言。成片不会为了凑尺寸拉伸或裁切落版。
- 源片已经烧了字幕：说明保留原字幕，还是提供无字幕原片。不会叠两层。
- 要无字幕版：说「要一版不带字幕的」，字幕轨仍保留在工程里，SRT 照常给。
- 图解想放进 Premiere Pro：先说一声，需要装 Premiere Pro MCP 服务。

## 安装

需要 Node.js 22+ 和 FFmpeg。装到 opencode 全局技能目录：

```bash
npx skills add https://github.com/zzh-editor/MAXs_VideoEditor \
  --skill video-edit --global --agent opencode --copy --yes
```

首次使用前检查依赖，只补缺少项。`skills` CLI 可能把副本放在 `~/.agents/skills/` 或 `~/.config/opencode/skills/`，按安装输出里的实际目录执行：

```bash
SKILL_DIR="$HOME/.agents/skills/video-edit"
test -f "$SKILL_DIR/SKILL.md" || SKILL_DIR="$HOME/.config/opencode/skills/video-edit"
python3 "$SKILL_DIR/scripts/ensure_dependencies.py" --check
python3 "$SKILL_DIR/scripts/ensure_dependencies.py" --install-missing
```

渲染需要 Chrome Headless Shell，可运行 `npx hyperframes doctor --json` 检查，缺浏览器时运行 `npx hyperframes browser ensure`。Premiere Pro、MCP 服务和 Bridge 只在导入图解到 Premiere 时需要，不影响剪辑和渲染。

## 仓库内容与技术说明

依赖按来源仓库分组安装，清单在 [`skills/video-edit/references/dependencies.json`](skills/video-edit/references/dependencies.json)。HyperFrames 的格式、动画、音频与 Studio 说明合并进 `hyperframes` / `hyperframes-cli`。账号色彩、安全框、字幕规范、图解规则和 4 组可编辑 SVG 原稿及对应 PNG 预览都随 `video-edit` 安装；图解以包内规则和 SVG 为准，`diagram-design`、`lieflat-charts`、`pixelfx` 只是可选补充，不阻塞安装。首次安装可能克隆较大的 HyperFrames 仓库，脚本默认把克隆超时设为 10 分钟。

仓库自带 MiSans VF、技研Labs 片头 Swoosh、剪辑与字幕脚本、参考文档和测试。剪辑规则入口是 [`skills/video-edit/SKILL.md`](skills/video-edit/SKILL.md)，细则在 [`skills/video-edit/references/`](skills/video-edit/references/)。

在仓库根目录运行检查：

```bash
python3 -m unittest discover -s skills/video-edit/tests
python3 skills/video-edit/scripts/ensure_dependencies.py --check
```

`lieflat-charts` 是可选参考，使用 PolyForm Noncommercial。本技能只引用其公开视觉原则，不复制代码、模板和素材；商业发布需遵守其许可证。仓库当前未声明整体许可证；MiSans VF 和 Swoosh 是随包的用户提供资产，公开分发或用于其他品牌前请先确认授权。Premiere Pro 服务和 MAXs 官方落版素材不随仓库提供，缺少时按需索取，不依赖个人电脑绝对路径。
