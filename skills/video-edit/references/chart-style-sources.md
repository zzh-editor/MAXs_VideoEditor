# 图表风格来源与使用边界

这些上游是图表审美和特效词汇的来源，不替代 `video-edit` 的品牌色、字幕位置、HyperFrames 时间线和可编辑交付规则。

## MAXs：Diagram Design

读取全局 `diagram-design` skill。MAXs 图表沿用它的编辑式结构：先判断语义关系再选图型，坐标与间距落在 4px 网格，密度克制，通常只留 1–2 个焦点，删掉不承载信息的节点和连线；不加阴影。

- 颜色和文字以 `brand-and-opening.md` 为准：MAXs 蓝 `#134FFF`、MiSans VF。Diagram Design 默认的橙色、字体和网页模板都不覆盖项目品牌。
- Diagram Design v2.6 增加了极坐标、瀑布、热力、结构变化和轴测图等类型；动效规则采用 `none/reveal/step/loop`，默认静帧完整，动效只解释顺序或变化，并考虑 reduced-motion。视频仍用 HyperFrames 的 seek-safe GSAP 时间线，不搬用滚动触发、点击控件或运行时 timer。
- MAXs 9:16 图表主体遵守 `brand-and-opening.md` 的红框安全区：`x=10%–88%`、`y=8%–59%`。节点、内部文字、图例、连接线和动画行程都须完整落在框内；视频/段落标题是独立标题位，不是图表主体。图表的首帧、中间帧和退场帧都不能越界。

## 技研Labs：Lieflat Charts

读取全局 `lieflat-charts` skill。按关系和阅读速度从 Lupi Editorial、Lupi Basics 等体系中找版式参考：真实节点与关系优先、单图单结论、线条和留白有秩序，避免等宽卡片堆叠。概念 b-roll 没有真实量值时，不把它硬套成数据图，也不编造数值。

- 颜色、字体和画幅规则仍以项目 `frame.md` 和 `brand-and-opening.md` 为准：`#ADF911`、MiSans VF、活动图解全画幅 `#161616`，底部字幕安全区留空。Lieflat 的四像素网格、单一重心、模板选择和色阶表达可作结构参考；用 HyperFrames 子组合重写，不搬 gallery 代码。
- Lieflat 当前规则偏快的 `quarticOut`、默认不弹跳、按序 stagger，并支持 `prefers-reduced-motion`。借用克制的节奏，不照搬网页 scroll/click 控制和毫秒级 stagger；按 HyperFrames 帧率与字幕阅读时间重排。
- `lieflat-charts` 使用 PolyForm Noncommercial，且其技能的成品流程另有署名提示。MAXs / 技研Labs 可能用于商业发布，所以只借鉴视觉原则，不调用它的整套产出流程，也不复制或随片分发其模板、HTML、代码或素材。用户要求直接复用这些资产时，先确认已有商业授权。

## 效果：PixelFX

当图表的知识点确实需要一次冲击、显现、消散、扫描或转场时，读取已安装的 `pixelfx` skill，并从该技能提供的 catalog / source checkout 搜索对应效果；不要依赖某台机器上的固定绝对路径：

1. 先用 `node tools/list.mjs <关键词>` 或 `docs/CATALOG.md` 找候选，阅读候选效果与 `meta.options`，再渲染预览并看过完整动作；不要只凭名字选。复用安装提供的源码，不把整库复制进视频项目。
2. 只用一个能解释当前图表关系的效果；可调整 `palette` 适配账号色，但 MAXs 蓝和技研Labs 绿仍由品牌规则决定。像素风格与内容不合时，只借用动作节奏并用原有图形重做，不硬贴 sprite。
3. 集成到 HyperFrames 时，使用本地素材或可由时间确定的绘制逻辑；不把 PixelFX 的 `update(dt)` 循环、`requestAnimationFrame`、未设种子的随机数或运行时网络请求带进最终组合。效果的图像与整段运动始终留在对应账号的图表安全框内。
4. 若分发改编的 PixelFX 代码或素材，保留源码仓库 `LICENSE` 与 `NOTICE.md` 要求；通常只用已审阅的效果参考，不复制整套库。

没有合适候选时回到 `hyperframes` 的原生动效参考，不为了凑效果加粒子或装饰。

## 上游更新

版本、commit 和最近检查日期记录在 `style-upstreams.json`。每次进入图表或动效设计分支时读取该文件；用户明确要求更新，或 `checked_at` 已满 7 天时：

1. 查询三个仓库 `main` 的 HEAD；用 `npx skills update diagram-design lieflat-charts pixelfx --global --yes` 更新全局 skill 副本。PixelFX 源码 checkout 若由其安装流程维护，按该 skill 的说明更新。
2. 只审阅与图型、视觉、动效、无障碍或输出契约相关的变化，按本文件边界更新图表规则；不让上游主题色覆盖账号颜色，也不覆盖 HyperFrames 或 MAXs 安全框规则。
3. 若上游重置了纯英文 description，按全局技能维护规则只翻译 description，保留技术名和触发词。所有查询成功后再更新 JSON 里的 `checked_at` 与 HEAD；任一网络检查失败时保留旧日期并报告未完成。

检查在下一次相关 `video-edit` 调用时触发，不运行后台定时任务。
