# 平台安全区

先选成片画幅和发布平台，再选安全框。区分三类范围：平台 UI 遮挡区、传统标题安全区、项目内部构图框。三者用途不同，不能拿一个百分比替代另一个。重要字幕、标题、图表节点和 CTA 按所选范围避让；背景与无关紧要的装饰可出框。

## 9:16 竖屏

下表像素按 1080×1920 换算。广告版位和普通投稿分开处理；平台会改 UI，发布前仍要用目标 App 预览。

| 目标 | 版式基准 | 来源和边界 |
|---|---|---|
| TikTok In-Feed 广告 | 优先下载与画幅、字幕行数、Anchor/互动组件匹配的官方 overlay。官方没有一个适用于所有广告的固定矩形。 | [TikTok Auction In-Feed Ads](https://ads.tiktok.com/help/article/video-ads-specifications)：安全区取决于尺寸、广告文案和附加格式，预览也可能与设备上的实况略有差异。排版初稿可参考 [AdKit 对标准 LTR 模板的量测](https://adkit.so/tools/safe-zones/tiktok)：上 240px、下 660px、左右各 120px；画面 y≥840px 时右侧 UI 区加宽至 300px。量测不是官方固定规格，Anchor、长文案和 Shop 卡片须换用各自模板。 |
| Instagram / Facebook Reels 与 Stories 广告 | 上 14%、下 35%、左右各 6%；有 disclaimer 的 Reels 广告底部留 40%。右下角互动按钮区另做切角，不按完整矩形放满字幕。 | [Meta Business Help](https://www.facebook.com/business/help/980593475366490) 提供 Safe Zone guardrail 和 9:16 遮挡说明。1080×1920 约为上 269px、下 672px、左右各 65px。 |
| YouTube Shorts 广告 | 按 Google 发布的 [竖屏广告 overlay PNG](https://services.google.com/fh/files/misc/youtubesafezoneoverlay_vertical_final.png) 排版；不要把安全区简化成只留左右边距的矩形。 | [Google Ads: About video ad specs](https://support.google.com/google-ads/answer/13547298) 说明不同广告版位、设备的 UI 遮挡各异，并提供官方 overlay。按 1080×1920 overlay 量测约为上 288px、下 672px、左 48px、右 192px。YouTube 没有公布一个适用于所有普通 Shorts 的固定像素框；广告 overlay 是保守参考，不是普通投稿规范。 |
| TikTok、Reels、Shorts 共用母版 | 重要内容取三个对应官方广告 overlay 的交集；下方还要避开 TikTok 右侧阶梯区。交集会较窄，图表密度应随之减少。 | 这是制作时的保守合成框，不是平台共同发布的标准。若内容因此读不清，分别输出平台版本。 |
| 抖音、快手、小红书、微信视频号、Bilibili 竖屏 | 未找到能确认的、公开且稳定的创作者 UI 安全区像素规范。先用平台当期投稿预览；文字和图表不要贴边，另避开右侧交互列、底部账号/文案/CTA 区。 | 不将 TikTok 广告 overlay 说成这些平台的官方规范。当前产品形态或投放组件变化时，用实机截图重画遮挡区。 |

MAXs 9:16 的图表框 `x=10%–88%`、`y=8%–59%` 是 PIP/图表构图规则，不等于平台 UI 安全区。两种规则同时适用时取交集；字幕仍按 `subtitle-handoff.md` 的 cue 位置放置。图表不能因避开 UI 而压入人脸或字幕带。

## 16:9 横屏

| 目标 | 版式基准 | 来源和边界 |
|---|---|---|
| YouTube 普通视频 | 关键文字和标识放在中央 90%（四边各留 5%）作为标题安全区；字幕避开底部约 10% 的控制条时段，右下角不放必须读到的小字。 | 90% 是[传统标题安全参考](https://eks.tv/title-safe-still-matters)，不是 YouTube 普通视频的官方 UI 遮挡框。播放控制会随鼠标、触屏状态出现或隐藏。 |
| Bilibili 普通横屏 | 1080p 初稿可按左右各约 80px、上方约 80px；字幕底边离画面底部 150–170px。长字幕控制在画宽 70% 内。 | 这些是[剪辑实践量测](https://www.lunxiao.com/article.html?id=24023)，不是 Bilibili 公布的创作者安全区。B 站播放器有弹幕、控制条等可变覆盖；[历史播放器帮助](https://web.archive.org/web/20140618204431/http://www.bilibili.com/html/help.html)曾描述“防挡字幕”会为字幕留底部 15%，不能保证当前所有客户端一致。 |
| Bilibili 弹幕友好版 | 在普通横屏字幕线基础上再向上留约 80px，字幕底边约在画面高度的 77%–79%；图表底部信息也不要放在弹幕密集带。 | 额外 80px 是[剪辑实践建议](https://www.lunxiao.com/article.html?id=24908)。弹幕横穿画面，单靠边缘安全框无法彻底避免遮挡；以关闭弹幕或防挡字幕后的实机预览复核。 |
| YouTube 横屏广告 | 使用 Google 发布的 [横屏广告 overlay PNG](https://services.google.com/fh/files/blogs/ytsafezoneoverlay-horizontal.png)，按其中的不规则切角和按钮区避让。 | [Google Ads: About video ad specs](https://support.google.com/google-ads/answer/13547298) 明确覆盖不同广告版位和屏幕；这套广告框不应套到普通视频。 |
| TikTok 横屏广告 | 下载与 16:9、文案长度、附加组件相符的 TikTok 官方 safe-zone ZIP。 | TikTok 给广告提供格式专用 overlay；不把它外推到普通 TikTok 投稿。 |

以下作为项目默认选择：技研Labs 16:9 图解继续遵守全画幅底色和底部 19% 字幕禁入带；MAXs 横屏若新增版本则按目标平台另选本表的标题/平台安全区。用户指定字幕 cue、既有品牌模板或平台模板时，以指定版本为准，并记录选择。

## 发布前检查

- 记录输出平台、画幅、安全区类型（平台 UI、标题安全或项目构图）和采用的边界。
- 多平台只交一个母版时，按各目标官方模板交集避让；交集过窄就拆平台版本。
- TikTok / Meta / Google 广告使用当期、对应版位的官方模板；普通投稿不要标成官方广告安全区。
- 抽查字幕、图表、脸部和 CTA 在最拥挤 UI 状态下仍完整。发布平台没有稳定公开参数时，明确标注为经验框并在实机预览确认。
