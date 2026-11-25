"""Map complete SRT cues, kept ranges, and an optional duplicated opening hook."""

import argparse
import json
from pathlib import Path
import re

STAMP = r"\d{2}:[0-5]\d:[0-5]\d,\d{3}"
CUE = re.compile(rf"(\d+)\n({STAMP}) --> ({STAMP})\n(.+)", re.S)


def milliseconds(stamp):
    hours, minutes, seconds, millis = map(int, re.split(r"[:,]", stamp))
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def timestamp(value):
    seconds, millis = divmod(value, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"


def parse_srt(text):
    text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        raise ValueError("字幕为空")
    cues = []
    previous_end = 0
    for block in re.split(r"\n[ \t]*\n", text):
        match = CUE.fullmatch(block.strip())
        if not match:
            raise ValueError(f"无效 SRT 条目: {block[:100]!r}")
        number, start, end, words = match.groups()
        start_ms, end_ms = milliseconds(start), milliseconds(end)
        if start_ms < previous_end or end_ms <= start_ms or not words.strip():
            raise ValueError(f"字幕 #{number} 时间重叠、逆序、时长为零或文字为空")
        cues.append((number, start_ms, end_ms, words))
        previous_end = end_ms
    return cues


def integer_ms(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} 必须为非负整数毫秒")
    return value


def parse_words(words_input):
    """Flatten word sidecars into [{word, start_ms, end_ms}, ...].

    兼容两种结构：
    - 扁平词表：[{"word": "跨", "start_ms": 1000, "end_ms": 1500}, ...]
    - video-transcribe 的 words.json：[{"text": ..., "words": [{"word": ..., "start": 1.18, "end": 1.52}]}, ...]
      段级条目里的秒制时间戳会展开成词级毫秒时间戳。
    """
    if not words_input:
        return []
    if isinstance(words_input, dict):
        words_input = words_input.get("words") or words_input.get("segments") or []
    if not isinstance(words_input, list):
        return []

    flat = []
    for item in words_input:
        if not isinstance(item, dict):
            continue
        nested = item.get("words")
        if isinstance(nested, list):
            flat.extend(nested)
        else:
            flat.append(item)

    res = []
    for w in flat:
        if not isinstance(w, dict):
            continue
        text = w.get("word", w.get("text", ""))
        if "start_ms" in w or "end_ms" in w:
            start = w.get("start_ms")
            end = w.get("end_ms")
        else:
            # video-transcribe / Whisper 用秒；other 工具可能用 start/end 但已是毫秒
            start = w.get("start")
            end = w.get("end")
            if isinstance(start, (int, float)) and isinstance(end, (int, float)):
                scale = w.get("time_unit") or w.get("unit")
                if scale != "ms":
                    start, end = start * 1000, end * 1000
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            continue
        if not text:
            continue
        w_copy = dict(w)
        w_copy["start_ms"] = int(round(start))
        w_copy["end_ms"] = int(round(end))
        w_copy["word"] = text
        res.append(w_copy)
    return res


def retime(plan, cues, words=None, allow_boundary_clip=False):
    required = {"source_duration_ms", "intro_ms", "keep"}
    allowed = required | {"hook_duplicate"}
    if not isinstance(plan, dict) or not required <= set(plan) or set(plan) - allowed:
        raise ValueError("清单需要 source_duration_ms, intro_ms, keep，可选 hook_duplicate")

    source_end = integer_ms(plan["source_duration_ms"], "source_duration_ms")
    cursor = integer_ms(plan["intro_ms"], "intro_ms")
    ranges = plan["keep"]
    if source_end == 0 or not isinstance(ranges, list) or not ranges:
        raise ValueError("源时长必须大于零，keep 必须为非空数组")

    words_list = parse_words(words)
    clips, mapped, retimed_words = [], [], []

    if "hook_duplicate" in plan:
        hook = plan["hook_duplicate"]
        keys = {"source_in_ms", "source_out_ms", "timeline_start_ms", "duration_ms"}
        if not isinstance(hook, dict) or set(hook) != keys:
            raise ValueError("hook_duplicate 仅接受 source_in_ms、source_out_ms、timeline_start_ms、duration_ms")
        hook_in = integer_ms(hook["source_in_ms"], "hook_duplicate.source_in_ms")
        hook_out = integer_ms(hook["source_out_ms"], "hook_duplicate.source_out_ms")
        hook_start = integer_ms(hook["timeline_start_ms"], "hook_duplicate.timeline_start_ms")
        hook_duration = integer_ms(hook["duration_ms"], "hook_duplicate.duration_ms")
        if hook_start != 0 or not hook_in < hook_out <= source_end:
            raise ValueError("hook_duplicate 必须从时间线 0 开始，且区间必须有效")
        if hook_duration != hook_out - hook_in:
            raise ValueError("hook_duplicate.duration_ms 必须等于源区间长度")
        if cursor != hook_duration:
            raise ValueError("intro_ms 必须等于 hook_duplicate.duration_ms")
        clips.append({
            "id": "hook",
            "start_ms": 0,
            "duration_ms": hook_duration,
            "media_start_ms": hook_in
        })

        if words_list:
            for w in words_list:
                if hook_in <= w["start_ms"] and w["end_ms"] <= hook_out:
                    rw = dict(w)
                    rw["start_ms"] = w["start_ms"] - hook_in
                    rw["end_ms"] = w["end_ms"] - hook_in
                    retimed_words.append(rw)

        for number, cue_start, cue_end, cue_text in cues:
            if cue_end <= hook_in or cue_start >= hook_out:
                continue
            if cue_start < hook_in or cue_end > hook_out:
                if allow_boundary_clip or words_list:
                    clip_in = max(cue_start, hook_in)
                    clip_out = min(cue_end, hook_out)
                    sub_words = [w for w in words_list if clip_in <= w["start_ms"] and w["end_ms"] <= clip_out] if words_list else []
                    txt = "".join(w["word"] for w in sub_words) if sub_words else cue_text
                    s_ms = clip_in - hook_in
                    e_ms = clip_out - hook_in
                    mapped.append((s_ms, e_ms, txt))
                else:
                    raise ValueError(f"字幕 #{number} 跨越 Hook 片段剪切点；先按实际词级语音拆分")
            else:
                mapped.append((cue_start - hook_in, cue_end - hook_in, cue_text))

    previous_out = 0
    for i, segment in enumerate(ranges, 1):
        if not isinstance(segment, dict) or set(segment) != {"in_ms", "out_ms"}:
            raise ValueError(f"保留段 #{i} 仅接受 in_ms 和 out_ms")
        start = integer_ms(segment["in_ms"], "in_ms")
        end = integer_ms(segment["out_ms"], "out_ms")
        if not previous_out <= start < end <= source_end:
            raise ValueError(f"保留段 #{i} 重叠、逆序、为空或超出源视频")
        duration = end - start
        clips.append({
            "id": f"source-{i}",
            "start_ms": cursor,
            "duration_ms": duration,
            "media_start_ms": start
        })

        if words_list:
            for w in words_list:
                if start <= w["start_ms"] and w["end_ms"] <= end:
                    rw = dict(w)
                    rw["start_ms"] = cursor + (w["start_ms"] - start)
                    rw["end_ms"] = cursor + (w["end_ms"] - start)
                    retimed_words.append(rw)

        for number, cue_start, cue_end, cue_text in cues:
            if cue_end <= start or cue_start >= end:
                continue
            if cue_start < start or cue_end > end:
                if allow_boundary_clip or words_list:
                    clip_in = max(cue_start, start)
                    clip_out = min(cue_end, end)
                    sub_words = [w for w in words_list if clip_in <= w["start_ms"] and w["end_ms"] <= clip_out] if words_list else []
                    txt = "".join(w["word"] for w in sub_words) if sub_words else cue_text
                    s_ms = cursor + (clip_in - start)
                    e_ms = cursor + (clip_out - start)
                    mapped.append((s_ms, e_ms, txt))
                else:
                    raise ValueError(f"字幕 #{number} 跨越保留段 #{i} 的剪切点；先按实际词级语音拆分")
            else:
                mapped.append((cursor + (cue_start - start), cursor + (cue_end - start), cue_text))
        cursor += duration
        previous_out = end

    mapped.sort(key=lambda item: (item[0], item[1]))
    output_cues = []
    previous_end = 0
    for start, end, text in mapped:
        if start < previous_end:
            raise ValueError("重映射后字幕时间轴存在交叠")
        output_cues.append(f"{len(output_cues) + 1}\n{timestamp(start)} --> {timestamp(end)}\n{text}")
        previous_end = end

    manifest = {"duration_ms": cursor, "clips": clips}
    retimed_srt = ("\n\n".join(output_cues) + "\n") if output_cues else ""
    return manifest, retimed_srt, retimed_words


def main():
    parser = argparse.ArgumentParser(description="Map SRT cues to retimed video.")
    parser.add_argument("plan", type=Path, help="Path to edit plan JSON")
    parser.add_argument("srt", type=Path, help="Path to input SRT file")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory to save output files")
    parser.add_argument("--words", type=Path, default=None, help="Path to optional words JSON file")
    parser.add_argument("--allow-boundary-clip", action="store_true", default=False, help="Automatically clip cues across keep boundaries")
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    cues = parse_srt(args.srt.read_text(encoding="utf-8"))

    words = None
    if args.words:
        words = json.loads(args.words.read_text(encoding="utf-8"))

    try:
        timeline, retimed_srt, retimed_words = retime(
            plan, cues, words=words, allow_boundary_clip=args.allow_boundary_clip)
        if not retimed_srt:
            raise ValueError("所有字幕均落在删除范围内；请核对清单与字幕时间原点")
        args.output_dir.mkdir(parents=True, exist_ok=False)
        (args.output_dir / "timeline.json").write_text(
            json.dumps(timeline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output_dir / "captions.srt").write_text(retimed_srt, encoding="utf-8")
        if args.words:
            (args.output_dir / "retimed_words.json").write_text(
                json.dumps(retimed_words, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"retime: {error}\n")
    print(f"{args.output_dir}: {len(timeline['clips'])} 段，{timeline['duration_ms']} ms")


if __name__ == "__main__":
    main()

