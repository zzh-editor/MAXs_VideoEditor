import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ensure_dependencies.py"
SKILL_DIR = SCRIPT.parents[1]
SPEC = importlib.util.spec_from_file_location("ensure_dependencies", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DependencyTests(unittest.TestCase):
    def test_manifest_requires_editing_skills_but_not_optional_style_sources(self):
        manifest = json.loads((SKILL_DIR / "references" / "dependencies.json").read_text())
        skills = {skill for source in manifest["sources"] for skill in source["skills"]}
        optional = {"general-video", "hyperframes-core", "hyperframes-animation",
                    "hyperframes-keyframes", "hyperframes-audio", "hyperframes-studio",
                    "hyperframes-creative", "diagram-design", "lieflat-charts", "pixelfx"}
        self.assertTrue(optional.isdisjoint(skills))
        self.assertTrue({"hyperframes", "hyperframes-cli", "hyperframes-registry", "media-use"}.issubset(skills))
        self.assertTrue((SKILL_DIR / "references/chart-style-sources.md").is_file())
        self.assertTrue((SKILL_DIR / "examples/diagrams/maxs-recruitment-pools.png").is_file())

    def test_required_local_assets_are_bundled(self):
        self.assertTrue((SKILL_DIR / "assets/fonts/MiSansVF.ttf").is_file())
        self.assertTrue((SKILL_DIR / "assets/audio/Swoosh_01.wav").is_file())
        self.assertTrue((SKILL_DIR / "assets/jiyan-opener.html").is_file())

    def test_authoritative_chart_sources_and_previews_are_bundled(self):
        self.assertTrue((SKILL_DIR / "references/chart-style-sources.md").is_file())
        examples = ["maxs-recruitment-pools", "maxs-study-timeline",
                    "jiyan-parent-child", "jiyan-model-pipeline"]
        for name in examples:
            for extension in ("svg", "png"):
                with self.subTest(example=name, extension=extension):
                    self.assertTrue((SKILL_DIR / f"examples/diagrams/{name}.{extension}").is_file())

    def test_jiyan_diagram_text_stays_above_caption_safe_band(self):
        for name in ["jiyan-parent-child", "jiyan-model-pipeline"]:
            source = (SKILL_DIR / f"examples/diagrams/{name}.svg").read_text()
            text_y = [int(value) for value in re.findall(r"<text\b[^>]*\by=\"(\d+)\"", source)]
            with self.subTest(example=name):
                self.assertTrue(text_y)
                self.assertLess(max(text_y), 820)

    def test_existing_skills_are_found_in_either_global_root(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = root / "config"
            agents = root / "agents"
            (config / "hyperframes" ).mkdir(parents=True)
            (config / "hyperframes" / "SKILL.md").touch()
            (agents / "pixelfx").mkdir(parents=True)
            (agents / "pixelfx" / "SKILL.md").touch()
            manifest = {"sources": [{"repository": "upstream/a", "skills": ["hyperframes"]},
                                     {"repository": "upstream/b", "skills": ["pixelfx"]}]}
            self.assertEqual(MODULE.missing_by_source(manifest, (config, agents)), {})

    def test_missing_skills_are_grouped_by_repository(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = {"sources": [{"repository": "upstream/a", "skills": ["one", "two"]},
                                     {"repository": "upstream/b", "skills": ["three"]}]}
            (root / "one").mkdir()
            (root / "one" / "SKILL.md").touch()
            self.assertEqual(MODULE.missing_by_source(manifest, (root,)),
                             {"upstream/a": ["two"], "upstream/b": ["three"]})

    def test_install_command_targets_opencode_global_scope(self):
        self.assertEqual(MODULE.install_command("owner/repo", ["one", "two"]), [
            "npx", "skills", "add", "owner/repo", "--global", "--agent", "opencode",
            "--skill", "one", "two", "--yes",
        ])

    def test_large_repository_timeout_has_a_safe_default_and_can_be_overridden(self):
        self.assertEqual(MODULE.install_environment({})["SKILLS_CLONE_TIMEOUT_MS"], "600000")
        self.assertEqual(MODULE.install_environment({"SKILLS_CLONE_TIMEOUT_MS": "900000"})[
            "SKILLS_CLONE_TIMEOUT_MS"], "900000")


if __name__ == "__main__":
    unittest.main()
