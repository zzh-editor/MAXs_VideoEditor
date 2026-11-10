# MAXs VideoEditor

`video-edit` 把录屏、直播回放或口播素材制作成可编辑的 HyperFrames 项目和 9:16 成片。当前技能版本：`1.1.9`。支持 MAXs、技研Labs 和 LeonaDesign。

## 安装

需要 Node.js 22+、FFmpeg 和 Chrome Headless Shell。

```bash
npx skills add https://github.com/zzh-editor/MAXs_VideoEditor \
  --skill video-edit --global --agent opencode --copy --yes
```

首次使用时检查并安装缺少的依赖：

```bash
SKILL_DIR="$HOME/.agents/skills/video-edit"
test -f "$SKILL_DIR/SKILL.md" || SKILL_DIR="$HOME/.config/opencode/skills/video-edit"
python3 "$SKILL_DIR/scripts/ensure_dependencies.py" --check
python3 "$SKILL_DIR/scripts/ensure_dependencies.py" --install-missing
```

## 开始一条视频

把视频路径发给 OpenCode，再说明已知信息。已有 SRT 或人工剪辑版时一并给出，技能会优先复用，不重做已完成的部分。

```text
用 video-edit 处理 /path/to/video.mp4。账号 MAXs，类型直播切片。保留已有人工剪辑和 captions.srt；图解先给我确认，检查和预览后再渲染。
```

素材原片有烧录字幕时，说明是保留原字幕还是提供无字幕版本。账号、类型、字幕处理、剪辑范围、图解授权和交付方式等未决选项会集中询问一次；你已经说清的字段不会重复问。

## 工作流程

1. **检查素材和工程。** 复用已有 HyperFrames 工程和有效 SRT；新工程默认放在源视频旁边。保留源视频、原始字幕和已有的手工编辑。
2. **确认剪辑与字幕。** 先确认删除范围，再对齐字幕。字幕只改成片副本，不覆盖原始 SRT；Studio 字幕轨和交付 SRT 来自同一份定稿。
3. **按口播安排画面。** 图表解释比较、流程和因果；大字报综合相邻字幕，不补字幕未支持的信息。全屏 A-roll 是口播常态，只有图解需要阅读时才缩成 PIP。PIP 覆盖超过 70% 或连续超过 30 秒会触发复查，不是硬性上限。
4. **渲染前检查。** 编辑时用 `npx hyperframes lint` 快速反馈；一批修改完成后运行完整 `npm run check`，再抽查首帧和改动图解的入场、中段、退场。检查通过后打开 HyperFrames 桌面应用预览。
5. **渲染和交付。** 你明确要求渲染，或事先授权后，技能直接渲染。成片默认烧录字幕；渲染成功后检查 `ffprobe` 和交付文件，不再抽查成片帧。

`renders/` 中每版成片都有同名 MP4、简体中文字幕 SRT 和 `_续编说明.txt`。同名文件已存在时改用下一个 `_v2`、`_v3` 版本，不覆盖旧文件。

## 在 HyperFrames 桌面应用中预览和编辑

在项目目录运行：

```bash
npx hyperframes preview --background
```

打开命令输出的网址。HyperFrames 桌面应用可以播放视频、定位时间线并手动编辑片段和图解；保存后改动会留在项目文件中。若随后要让 agent 继续修改，先在项目目录运行：

```bash
npx hyperframes catch-up
```

再把要改的位置和内容发给 agent。不要重新生成整个工程覆盖桌面应用中的编辑。

## 账号视觉

| 账号 | 主要规则 |
| --- | --- |
| MAXs | `#134FFF`、MiSans VF；9:16 图表在 `x=10%–88%`、`y=8%–59%` 安全框内。全屏 A-roll 为主，图解需要时使用右下角 PIP。 |
| 技研Labs | `#ADF911` 配黑字；课程和直播使用 `#161616` 全画幅图解底，底部保留至少 19% 字幕区。课程/直播使用固定透明片头，口播默认不加。 |
| LeonaDesign | `#FEF201` 配黑字；不复用其他账号的 Logo 或品牌素材。 |

所有图解和新增文字都要有字幕或课程材料依据。动效跟随口播 cue，使用可 seek 的确定性时间线；不添加装饰循环来填时长。

## 维护者

在仓库根目录检查技能包：

```bash
python3 -m unittest discover -s skills/video-edit/tests
python3 skills/video-edit/scripts/ensure_dependencies.py --check
```

详细的剪辑、字幕、图解和检查规则见 [`skills/video-edit/SKILL.md`](skills/video-edit/SKILL.md) 及 [`skills/video-edit/references/`](skills/video-edit/references/)。

## 致谢

本项目依赖多个开源项目；使用和再分发时需遵守各自许可：

- [HyperFrames](https://github.com/heygen-com/hyperframes)：时间线预览与视频渲染。
- [video-transcribe](https://github.com/zzh-editor/video-transcribe)：语音转写。
- [Srt-Enhancer](https://github.com/zzh-editor/Srt-Enhancer)：字幕润色。
- [diagram-design](https://github.com/cathrynlavery/diagram-design)：图型参考。
- [lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts)：排版参考，使用前需留意其非商业许可。
- [pixelfx](https://github.com/patch-gg/pixelfx)：可选图解特效。
- [Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP)：可选的 Premiere Pro 导入服务。
- [MiSans VF](https://hyperos.mi.com/font/zh/)：字体由小米提供。
