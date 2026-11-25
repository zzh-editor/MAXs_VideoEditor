import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "retime.py"
SPEC = importlib.util.spec_from_file_location("retime", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RetimeTests(unittest.TestCase):
    def plan(self):
        return {"source_duration_ms": 30000, "intro_ms": 2800,
                "keep": [{"in_ms": 10000, "out_ms": 18000},
                         {"in_ms": 21000, "out_ms": 30000}]}

    def test_cuts_and_intro_share_the_same_clock(self):
        cues = MODULE.parse_srt(
            "\ufeff1\r\n00:00:10,000 --> 00:00:18,000\r\n完整第一句\r\n\r\n"
            "2\r\n00:00:19,000 --> 00:00:20,000\r\n删除的声音\r\n\r\n"
            "3\r\n00:00:23,000 --> 00:00:24,000\r\nPython < 3\r\n第二行\r\n")
        timeline, srt, _ = MODULE.retime(self.plan(), cues)
        self.assertEqual(timeline["duration_ms"], 19800)
        self.assertEqual(timeline["clips"][1]["start_ms"], 10800)
        self.assertEqual(timeline["clips"][1]["media_start_ms"], 21000)
        self.assertEqual(MODULE.parse_srt(srt)[1][1:], (12800, 13800, "Python < 3\n第二行"))
        self.assertNotIn("删除的声音", srt)

    def test_partial_cue_is_not_compressed_or_duplicated(self):
        with self.assertRaisesRegex(ValueError, "跨越"):
            MODULE.retime(self.plan(), [("7", 17000, 23000, "这句话不能硬塞")])

    def test_overlay_title_adds_no_time(self):
        plan = {"source_duration_ms": 8000, "intro_ms": 0,
                "keep": [{"in_ms": 0, "out_ms": 3800},
                         {"in_ms": 5000, "out_ms": 8000}]}
        timeline, srt, _ = MODULE.retime(plan, [("1", 0, 2000, "开头语音仍同步")])
        self.assertEqual(timeline["duration_ms"], 6800)
        self.assertEqual(timeline["clips"][0]["start_ms"], 0)
        self.assertEqual(MODULE.parse_srt(srt)[0][1], 0)

    def test_hook_duplicate_prepends_video_and_duplicates_captions(self):
        plan = {"source_duration_ms": 30000, "intro_ms": 2000,
                "hook_duplicate": {"source_in_ms": 10000, "source_out_ms": 12000,
                                   "timeline_start_ms": 0, "duration_ms": 2000},
                "keep": [{"in_ms": 0, "out_ms": 30000}]}
        cues = [("1", 0, 1000, "body start"),
                ("2", 10000, 11000, "hook line one"),
                ("3", 11000, 12000, "hook line two"),
                ("4", 13000, 14000, "body later")]

        timeline, srt, _ = MODULE.retime(plan, cues)

        self.assertEqual(timeline["duration_ms"], 32000)
        self.assertEqual(timeline["clips"], [
            {"id": "hook", "start_ms": 0, "duration_ms": 2000, "media_start_ms": 10000},
            {"id": "source-1", "start_ms": 2000, "duration_ms": 30000,
             "media_start_ms": 0},
        ])
        self.assertEqual([(start, end, text) for _, start, end, text in MODULE.parse_srt(srt)], [
            (0, 1000, "hook line one"), (1000, 2000, "hook line two"),
            (2000, 3000, "body start"), (12000, 13000, "hook line one"),
            (13000, 14000, "hook line two"), (15000, 16000, "body later"),
        ])

    def test_hook_rejects_partial_caption_and_mismatched_intro(self):
        plan = {"source_duration_ms": 30000, "intro_ms": 2000,
                "hook_duplicate": {"source_in_ms": 10000, "source_out_ms": 12000,
                                   "timeline_start_ms": 0, "duration_ms": 2000},
                "keep": [{"in_ms": 0, "out_ms": 30000}]}
        with self.assertRaisesRegex(ValueError, "跨越"):
            MODULE.retime(plan, [("1", 11000, 12500, "跨越 Hook 边界")])
        with self.assertRaisesRegex(ValueError, "intro_ms"):
            MODULE.retime({**plan, "intro_ms": 1999}, [])

    def test_words_drive_boundary_clip_and_retimed_words(self):
        plan = {"source_duration_ms": 4000, "intro_ms": 0,
                "keep": [{"in_ms": 0, "out_ms": 1500},
                         {"in_ms": 2500, "out_ms": 4000}]}
        cues = [("1", 1000, 3000, "跨越剪切点")]
        words = [{"word": "跨", "start_ms": 1000, "end_ms": 1500},
                 {"word": "越", "start_ms": 1500, "end_ms": 2500},
                 {"word": "剪", "start_ms": 2500, "end_ms": 3000}]
        timeline, srt, retimed_words = MODULE.retime(
            plan, cues, words=words, allow_boundary_clip=True)
        self.assertEqual(timeline["duration_ms"], 3000)
        self.assertEqual([(start, end, text) for _, start, end, text in MODULE.parse_srt(srt)],
                         [(1000, 1500, "跨"), (1500, 2000, "剪")])
        self.assertEqual([(w["start_ms"], w["end_ms"], w["word"]) for w in retimed_words],
                         [(1000, 1500, "跨"), (1500, 2000, "剪")])

    def test_video_transcribe_segment_sidecar_is_flattened_to_ms(self):
        sidecar = [
            {"start": 0.0, "end": 2.78, "text": "大家好,今天",
             "words": [{"word": "大家好,", "start": 0.0, "end": 1.18},
                       {"word": "今天", "start": 1.18, "end": 1.52}]},
            {"start": 2.78, "end": 4.0, "text": "我们来聊",
             "words": [{"word": "我们", "start": 2.78, "end": 3.2},
                       {"word": "来聊", "start": 3.2, "end": 4.0}]},
        ]
        self.assertEqual(
            [(w["word"], w["start_ms"], w["end_ms"]) for w in MODULE.parse_words(sidecar)],
            [("大家好,", 0, 1180), ("今天", 1180, 1520),
             ("我们", 2780, 3200), ("来聊", 3200, 4000)])

    def test_words_dict_with_segments_key_is_accepted(self):
        sidecar = {"segments": [{"words": [{"word": "嗯", "start": 0.25, "end": 0.5}]}]}
        self.assertEqual([(w["word"], w["start_ms"], w["end_ms"]) for w in MODULE.parse_words(sidecar)],
                         [("嗯", 250, 500)])
        self.assertEqual(MODULE.parse_words([{"word": "", "start": 1, "end": 2}]), [])

    def test_invalid_ranges_are_rejected(self):
        for ranges in [[], [{"in_ms": 2, "out_ms": 2}],
                       [{"in_ms": -1, "out_ms": 4}],
                       [{"in_ms": 0, "out_ms": 30001}],
                       [{"in_ms": 10, "out_ms": 20}, {"in_ms": 19, "out_ms": 25}],
                       [{"in_ms": 20, "out_ms": 25}, {"in_ms": 10, "out_ms": 15}],
                       [{"in_ms": 0, "out_ms": 20, "rate": 2}]]:
            with self.subTest(ranges=ranges), self.assertRaises(ValueError):
                MODULE.retime({**self.plan(), "keep": ranges}, [])

    def test_noninteger_time_is_rejected(self):
        for value in [True, -1, 2.8, float("nan"), "2800"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                MODULE.retime({**self.plan(), "intro_ms": value}, [])

    def test_invalid_subtitles_are_rejected(self):
        for text in ["", "1\n00:61:00,000 --> 00:62:00,000\n错误",
                     "1\n00:00:02,000 --> 00:00:01,000\n逆序",
                     "1\n00:00:00,000 --> 00:00:02,000\n甲\n\n"
                     "2\n00:00:01,000 --> 00:00:03,000\n乙"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                MODULE.parse_srt(text)

    def test_long_timestamp_roundtrip(self):
        self.assertEqual(MODULE.milliseconds(MODULE.timestamp(360000001)), 360000001)

    def test_cli_preserves_existing_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "plan.json").write_text(
                '{"source_duration_ms":2000,"intro_ms":0,"keep":[{"in_ms":0,"out_ms":2000}]}')
            (root / "source.srt").write_text("1\n00:00:00,000 --> 00:00:01,000\n保留\n")
            output = root / "mapped"
            output.mkdir()
            marker = output / "captions.srt"
            marker.write_text("用户已编辑")
            result = subprocess.run([sys.executable, str(SCRIPT), str(root / "plan.json"),
                                     str(root / "source.srt"), "--output-dir", str(output)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(marker.read_text(), "用户已编辑")


if __name__ == "__main__":
    unittest.main()
