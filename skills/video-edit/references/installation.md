# 安装与依赖

仓库中的 `skills/video-edit/` 是可安装 skill。OpenCode 全局安装：

```bash
npx skills add https://github.com/zzh-editor/MAXs_VideoEditor \
  --skill video-edit --global --agent opencode --copy --yes
```

安装器可能把副本放在 `~/.agents/skills/` 或 `~/.config/opencode/skills/`。以下命令先检查两种常见位置，再运行依赖检查：

```bash
SKILL_DIR="$HOME/.agents/skills/video-edit"
test -f "$SKILL_DIR/SKILL.md" || SKILL_DIR="$HOME/.config/opencode/skills/video-edit"
python3 "$SKILL_DIR/scripts/ensure_dependencies.py" --check
```

检查后只补缺少项：

```bash
SKILL_DIR="$HOME/.agents/skills/video-edit"
test -f "$SKILL_DIR/SKILL.md" || SKILL_DIR="$HOME/.config/opencode/skills/video-edit"
python3 "$SKILL_DIR/scripts/ensure_dependencies.py" --install-missing
```

依赖按 `references/dependencies.json` 的来源仓库分组安装。HyperFrames 已将 `general-video` 并入 `hyperframes`，不再单独安装已退役的 skill。MAXs 与技研Labs 风格、安全框、字幕交接和导入规则都包含在本仓库。首次安装可能需要克隆较大的 HyperFrames 仓库；脚本默认给 skills CLI 10 分钟，网络较慢时可把 `SKILLS_CLONE_TIMEOUT_MS` 设得更长。

## 随包资源与外部要求

- `assets/fonts/MiSansVF.ttf` 和 `assets/audio/Swoosh_01.wav` 已包含在仓库，项目引用本地副本。
- 渲染需要 Node.js 22+、FFmpeg 和 HyperFrames 支持的 Chrome Headless Shell。可运行 `npx hyperframes doctor --json` 检查；缺少浏览器时运行 `npx hyperframes browser ensure`。
- `premiere-pro-mcp` skill 只用于 Premiere 导入步骤；Premiere Pro、MCP 服务和 Bridge 是可选项，不影响基本剪辑与 MP4 渲染。
- MAXs 官方落版素材不在仓库。需要落版时使用者需提供获准使用的素材；技能不引用个人电脑上的固定绝对路径。
- `lieflat-charts` 上游采用 PolyForm Noncommercial。技能只引用其视觉原则，不复制或打包其代码、模板和素材；商业项目需遵守其许可证说明。
