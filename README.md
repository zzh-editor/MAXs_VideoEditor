# MAXs VideoEditor

`video-edit` 是 OpenCode 的 HyperFrames 剪辑 skill：把课程录屏、直播回放或口播素材做成可编辑工程和 9:16 成片，覆盖 MAXs、技研Labs、LeonaDesign 三个账号。

当前版本：`1.3.2`。

本地仓库：`/Users/rubber/Documents/Rubber/Skill_Dev`（所有自研 skill 的唯一仓库）。
安装副本：`~/.agents/skills/video-edit`。

## 安装

需要 Node.js 22+、FFmpeg 和 Chrome Headless Shell。

```bash
npx skills add https://github.com/zzh-editor/MAXs_VideoEditor \
  --skill video-edit --global --agent opencode --copy --yes
```

首次使用前检查依赖，只补缺少项：

```bash
SKILL_DIR="$HOME/.agents/skills/video-edit"
test -f "$SKILL_DIR/SKILL.md" || SKILL_DIR="$HOME/.config/opencode/skills/video-edit"
python3 "$SKILL_DIR/scripts/ensure_dependencies.py" --check
python3 "$SKILL_DIR/scripts/ensure_dependencies.py" --install-missing
```

渲染还需要浏览器：`npx hyperframes doctor --json` 检查，缺浏览器时 `npx hyperframes browser ensure`。Premiere Pro 导入是可选步骤，不影响剪辑和渲染。

## 第一条视频

把视频路径发给 OpenCode，再补充已知信息。已有 SRT、人工剪辑版或现成 HyperFrames 工程时一并说明，技能会优先复用。

```text
用 video-edit 处理 /path/to/video.mp4。账号 MAXs，直播切片。保留已有人工剪辑和 captions.srt；图解先给我确认，检查和预览后再渲染。
```

未决事项（账号、类型、剪辑范围、转写/润色、图解授权、交付方式）会按 `references/preflight.md` **一次性问完**并写入 `BRIEF.md`；你已说清的字段不会重复问，下游 `video-transcribe`、`srt-enhancer` 也不会再问一遍。

## 工作流

1. **导入与一次性确认。** 检查媒体信息、同目录 SRT、已有工程和源片烧录文字；工程默认放 `<视频文件名>-hyperframes/`。
2. **原始索引。** 用户给的 SRT 为文本来源；有效就复用，缺可靠字幕才调 `video-transcribe`。
3. **保守精剪。** 口吃、自纠改口、说完又否定的重复默认列入删除；伤论点或指代时才保留并写明原因。VAD/静音只给候选。🔴 只在问卷预批准范围内执行，超出时只问差异项。
4. **字幕对时。** 按同一剪辑清单调 `scripts/retime.py`；跨剪切点用可靠词级时间，词级数据复用 `video-transcribe` 的引擎（不另建转写环境）。引擎不可用就保留整句或挂起待确认，**不改时间戳把条目塞进保留区间**。
5. **内容扫描与 b-roll 提案。** 字幕定稿后必做一次，生成精简 cue-map 复用；候选写清字幕编号、源时间、主张、时长、受众标签与数字 cue。🔴 授权按问卷预批准处理，否则停下问。
6. **包装与图解。** 图表文案按 `references/copy-writing.md` 七条与交付前四问；标题写观众所得、一图一结论、数字走 `BRIEF.md` 口径、`cards.json` 记 `number_cue`/`claim_cue`。标题是问句或前 15 秒抛问句时用提问卡两段式，全片只做一次。相邻图解段停留会超 5 秒时先回全屏 A-roll。
7. **检查与交付。** 迭代用 `lint`，一批改完或出片前跑 `check --json`；通过后抽首帧和受影响图解的入场/中段/退场读图。然后 `npx hyperframes preview --background` 交 URL，预览不等于验收。授权后渲染，成功后只用 `ffprobe` 核对容器信息和配套 SRT 同源。

## 交付物

`renders/` 下每版一套：MP4（默认烧录字幕）+ 同名简体 SRT + `_续编说明.txt`。同名文件已存在时递增 `_v2`、`_v3`，不覆盖旧件。源视频、原始 SRT 和 Studio 里的手工编辑都不覆盖。

## 账号视觉

| 账号 | 主要规则 |
| --- | --- |
| MAXs | `#134FFF`、MiSans VF；9:16 图表在 `x=10%–88%`、`y=8%–59%` 安全框内。全屏 A-roll 为常态，图解需要阅读时才缩右下 PIP。 |
| 技研Labs | `#ADF911` 配黑字；图解用 `#161616` 全画幅底，底部留至少 19% 字幕带。课程/直播用固定透明片头，口播默认不加。 |
| LeonaDesign | `#FEF201` 配黑字；不复用其他账号的 Logo 与品牌素材。 |

所有图解与新增文字都要有字幕或课程材料依据；动效跟随口播 cue，用可 seek 的确定性时间线，不用循环动画填时长。

## 预览与续编

```bash
npx hyperframes preview --background
```

打开输出网址即可在 HyperFrames Studio 里播放、定位时间线和手改片段。改完要让 agent 继续接手，先在项目目录跑。

```bash
npx hyperframes catch-up
```

再把改动位置发过来；不要整项目重建覆盖 Studio 里的编辑。

## 维护

在仓库根目录：

```bash
python3 -m unittest discover -s skills/video-edit/tests
python3 skills/video-edit/scripts/ensure_dependencies.py --check
python3 ~/.agents/skills/darwin-skill/scripts/darwin.py check skills/video-edit
```

最后一条是 Darwin 的零 token 体检（frontmatter、引用可达、体积、安全）。本 skill 的进化记录在 `~/.agents/skills/darwin-skill/results.tsv`。

改完仓库内容后同步到安装副本：

```bash
rsync -a --exclude '__pycache__' --exclude '.DS_Store' \
  skills/video-edit/ ~/.agents/skills/video-edit/
```

## 目录

```text
skills/video-edit/
├── SKILL.md              主流程与硬约束
├── references/           问卷、精剪、字幕、品牌、图解、文案、cue-map、安装等细则
├── scripts/              retime.py（剪辑映射）、ensure_dependencies.py
├── assets/               MiSans VF、Swoosh、技研片头、续编说明模板
├── examples/diagrams/    4 组 SVG 原稿与 PNG 预览
├── evals/ tests/         回归用例与单测
└── trigger-tests.json    description 触发测试
```

## 致谢

使用和再分发依赖时需遵守各自许可：

- [HyperFrames](https://github.com/heygen-com/hyperframes)：时间线预览与渲染。
- [video-transcribe](https://github.com/zzh-editor/video-transcribe)：语音转写与词级时间。
- [Srt-Enhancer](https://github.com/zzh-editor/Srt-Enhancer)：字幕润色与断句。
- [diagram-design](https://github.com/cathrynlavery/diagram-design)：图型参考。
- [lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts)：排版参考（PolyForm Noncommercial，仅引用视觉原则）。
- [pixelfx](https://github.com/patch-gg/pixelfx)：可选图解特效。
- [Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP)：可选的 Premiere 导入服务。
- [MiSans VF](https://hyperos.mi.com/font/zh/)：字体由小米提供。

仓库未声明整体许可证。MiSans VF 与 Swoosh 是随包的用户提供资产，公开分发前请先确认授权。
