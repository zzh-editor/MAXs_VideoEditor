"""Map complete SRT cues, kept ranges, and an optional duplicated opening hook."""

import argparse
import json
from pathlib import Path
import re


STAMP = r"\d{2,}:[0-5]\d:[0-5]\d,\d{3}"
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
            raise ValueError(f"无效 SRT 条目：{block[:100]!r}")
        number, start, end, words = match.groups()
        start, end = milliseconds(start), milliseconds(end)
        if start < previous_end or end <= start or not words.strip():
            raise ValueError(f"字幕 #{number} 时间重叠、逆序、时长为零或文字为空")
        cues.append((number, start, end, words))
        previous_end = end
    return cues


def integer_ms(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} 必须为非负整数毫秒")
    return value


def retime(plan, cues):
    required = {"source_duration_ms", "intro_ms", "keep"}
    allowed = required | {"hook_duplicate"}
    if not isinstance(plan, dict) or not required <= set(plan) or set(plan) - allowed:
        raise ValueError("清单需要 source_duration_ms、intro_ms、keep，可选 hook_duplicate")
    source_end = integer_ms(plan["source_duration_ms"], "source_duration_ms")
    cursor = integer_ms(plan["intro_ms"], "intro_ms")
    ranges = plan["keep"]
    if source_end == 0 or not isinstance(ranges, list) or not ranges:
        raise ValueError("源时长必须大于零，keep 必须为非空数组")
    if any(end > source_end for _, _, end, _ in cues):
        raise ValueError("字幕超出源视频时长")
    clips, mapped = [], []
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
            raise ValueError("hook_duplicate 必须从时间线 0 开始，且源区间必须有效")
        if hook_duration != hook_out - hook_in:
            raise ValueError("hook_duplicate.duration_ms 必须等于源区间长度")
        if cursor != hook_duration:
            raise ValueError("intro_ms 必须等于 hook_duplicate.duration_ms")
        clips.append({"id": "hook", "start_ms": 0, "duration_ms": hook_duration,
                      "media_start_ms": hook_in})
        for number, cue_start, cue_end, words in cues:
            if cue_end <= hook_in or cue_start >= hook_out:
                continue
            if cue_start < hook_in or cue_end > hook_out:
                raise ValueError(f"字幕 #{number} 跨越 Hook 片段剪切点；先按实际词级语音拆分")
            mapped.append((cue_start - hook_in, cue_end - hook_in, words))
    previous_out = 0
    for i, segment in enumerate(ranges, 1):
        if not isinstance(segment, dict) or set(segment) != {"in_ms", "out_ms"}:
            raise ValueError(f"保留段 #{i} 仅接受 in_ms 和 out_ms")
        start = integer_ms(segment["in_ms"], "in_ms")
        end = integer_ms(segment["out_ms"], "out_ms")
        if not previous_out <= start < end <= source_end:
            raise ValueError(f"保留段 #{i} 重叠、逆序、为空或超出源视频")
        clips.append({"id": f"source-{i}", "start_ms": cursor,
                      "duration_ms": end - start, "media_start_ms": start})
        for number, cue_start, cue_end, words in cues:
            if cue_end <= start or cue_start >= end:
                continue
            # shortcut: partial cues need reviewed word-level splits before mapping.
            if cue_start < start or cue_end > end:
                raise ValueError(f"字幕 #{number} 跨越保留段 #{i} 的剪切点；先按实际词级语音拆分")
            mapped.append((cursor + cue_start - start, cursor + cue_end - start, words))
        cursor += end - start
        previous_out = end
    srt = "\n\n".join(
        f"{i}\n{timestamp(start)} --> {timestamp(end)}\n{words}"
        for i, (start, end, words) in enumerate(mapped, 1)
    )
    return {"duration_ms": cursor, "clips": clips}, srt + ("\n" if srt else "")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("srt", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8-sig"))
        cues = parse_srt(args.srt.read_text(encoding="utf-8-sig"))
        timeline, srt = retime(plan, cues)
        if not srt:
            raise ValueError("所有字幕均落在删除范围内；请核对清单与字幕时间原点")
        args.output_dir.mkdir(parents=True, exist_ok=False)
        (args.output_dir / "timeline.json").write_text(
            json.dumps(timeline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output_dir / "captions.srt").write_text(srt, encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"retime: {error}\n")
    print(f"{args.output_dir}: {len(timeline['clips'])} 段，{timeline['duration_ms']} ms")


if __name__ == "__main__":
    main()
