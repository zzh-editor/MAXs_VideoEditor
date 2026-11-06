# 渲染后导入 Premiere Pro

只在渲染完成、文件验证通过后询问；用户明确同意“导入当前 Premiere Pro 工程”后才执行。拒绝或未回复时保留 HyperFrames 项目和渲染文件，不改 Premiere 工程。

1. 先调用 `verify_premiere_connection`。如果结果带 `retry: false` 和 `userActionRequired: true`，逐字转达 `nextStep`，停止所有 Premiere 工具调用；不要重试或绕过 Bridge。
2. 只读检查当前工程、活动序列、字幕轨和视频轨。确认当前工程就是本次素材对应工程；若工程或序列不明确，让用户在 Premiere 打开正确项目后再继续。不要自行切换、创建或关闭工程。
3. 每个图解子组合单独渲染一个文件。技研Labs 全画幅图解默认导出无声 MP4；用户选了透明叠加时再导出 WebM。依据 `cards.json` 取图解 ID、时长和 `timeline_start`，不要把包含长空档的总时间线渲染件误当成单段图解。验证文件非空、时长和画幅符合子组合后，将文件移动到当前 `.prproj` 同级的 `hyperframes/` 目录，不能覆盖同名文件。
4. 在 Premiere 项目面板创建或复用 `hyperframes` bin，导入这些本地文件，再把项目项移入该 bin。按读取到的轨道结构，把图解放到 A-Roll 上方、可见字幕轨下方的独立视频轨；不得覆盖现有片段或移动字幕。每段的入点用 `cards.json` 的 `timeline_start`，视频不带音频。
5. 读回 bin 项目项和目标序列轨道，逐段核对路径、起点、时长和目标轨道后再保存工程。核对失败就停止，不声称导入完成；文件已移动时保留在 `hyperframes/`，把路径和失败原因告诉用户。

MCP 工具名和参数先用 `search_tools` / `get_tool_schema` 查询，再调用对应工具。不得凭记忆拼工具名或参数。导入确认同时授权本流程中的文件移动、bin 创建、序列插入和保存；若发现将覆盖现有文件、遮住字幕或改动 A-Roll，先暂停并询问。
