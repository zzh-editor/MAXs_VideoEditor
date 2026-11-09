# HyperFrames 口播剪辑参考

主索引：[HyperFrames `llms.txt`](https://hyperframes.heygen.com/llms.txt)。该索引列出 Docs 134 页和 Catalog 449 页。本参考按其 `examples#talking-head-edits`、talking-head 字幕指南和动画文档整理，重点采用可落到现有 `video-edit` 管线的规则。

## 口播画面的组织

- HyperFrames Inspiration 的 Talking-head edits 用短视频常见剪辑、字幕、cutaway、callout 和节奏作参考。具体制作范例集中在 [Captions and recuts](https://hyperframes.heygen.com/guides/captions-and-recuts.md)；首页该栏目本身是灵感分类，不是逐项规格表。
- 原声和审核过的剪辑保持一条时间基准。要剪静默或重排时，先确认最终剪辑，再按它重算字幕；默认 verbatim rail 承载口播全文，内容和语气适合时才挑少数关键词作 emphasis。
- 重点词做 speaker-behind embed 是稀有峰值，需先抠出人像，让文字置于人物后层；每个 beat 至多一个、不可同时出现两个，最多选一个全片 apex。普通讲解优先清晰字幕 rail；MAXs 仍禁止独立漂浮花字，遵循品牌规则。
- 设计卡片与逐字稿主张和时间同步。先明确卡片内容、出现时刻、持续时间及说话人如何分享画幅：full-bleed、split、PiP 或 overlay。图形不得挡脸或关键实拍内容；双人、多机位或硬切素材按镜头/说话人分段处理。
- lower third 需要确切文案、入点和完整退场时间；叠在实拍上时优先无底卡样式，背景繁杂或亮度高到影响可读性时再用实底。透明素材只在确实需要叠加时使用，并检查首尾帧清空。
- 图解需要全屏时，把 A-Roll、跟随人物的标题贴片和遮罩放进同一个变换容器，用 `fromTo()` 关键帧将整组从全屏移到 PIP，再在图解结束时移回全屏。MAXs 竖屏的 PIP 落在右下角 312×555（`x: 740, y: 1337, scale: 0.288889`，距右、下各 28px），`0.4s power2.inOut`，写死在 `brand-and-opening.md`；进、出两个方向都要有双向关键帧，不能只切布局或只动图解。贴片必须跟随 A-Roll 并继续遮住源画面里的旧贴片。两个方向都检查中间帧和边界帧，确保可 seek、无空帧。
- MAXs 源片包装时抽 3–5 帧定位左侧福利卡的文字范围，再按这一条源片实际位置确定标题板尺寸；不同视频不复用固定坐标。标题完整盖住卡片和底栏，源片其他文字不擅自遮。不要自动添加推拉变焦；只有用户要求时才做，并在用户否定后只撤销新增推拉，保留原有图解 PIP 动画及 Studio 编辑。

## 动效与 HyperFrames 时间线

- 每张短图解讲一个视觉主张，按口播拍点安排变化。进入后让已读懂的元素停住，只继续动正在变化的量或关系；不为“活跃”而给所有元素呼吸动画。高潮特效只落一个有依据的 beat。
- 普通 motion graphic 通常少于 10 秒，最长约 30 秒；短概念不拉长凑时长。按屏幕文字实际可读时间留 hold，片头和退场都有明确终态。
- GSAP 时间线必须 `paused: true`，注册到匹配 `data-composition-id` 的 `window.__timelines`。给重要 tween 写显式时间位置；需要可靠随机 seek 时用 `fromTo()` 固定两端；优先变换和透明度，不反复动画布局属性。媒体播放和 seek 交给 HyperFrames data attributes，不从 GSAP 操纵 `<video>` / `<audio>`。
- 动效、程序绘制和随机变化必须可由当前时间帧重建。禁止用实时播放状态、`requestAnimationFrame`、`Date.now()`、计时器或未设种子的随机数驱动最终画面。完成后运行项目 `check`，抽查首帧、运动中帧和最后一帧；静态播放顺畅不能代替 seek 检查。
- 文字始终可读，字幕、图表和 callout 服从 `platform-safe-areas.md` 与账号专属布局。安全框检查动画全程路径，而不只查首尾位置。

## 上游页面

- [Inspiration / Talking-head edits](https://hyperframes.heygen.com/examples#talking-head-edits)
- [Captions and recuts](https://hyperframes.heygen.com/guides/captions-and-recuts.md)
- [Motion graphics](https://hyperframes.heygen.com/guides/motion-graphics.md)
- [Motion vocabulary](https://hyperframes.heygen.com/prompting/motion.md)
- [GSAP animation contract](https://hyperframes.heygen.com/guides/gsap-animation.md)
- [Caption components](https://hyperframes.heygen.com/prompting/captions-catalog.md)
- [Reference any video](https://hyperframes.heygen.com/studio-app/reference-video.md)

检查日期：2026-11-03。
