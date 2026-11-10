"""Pipeline Optimization Toolkit: cue extractor, SVG validator, and declarative renderer."""

import argparse
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

BRAND_COLORS = {
    "maxs": "#134FFF",
    "jiyan": "#ADF911",
    "leona": "#7C3AED"
}


def parse_srt_cues(srt_text):
    cues = []
    blocks = re.split(r"\n[ \t]*\n", srt_text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n").strip())
    stamp_pattern = re.compile(r"(\d+)\n(\d{2}:[0-5]\d:[0-5]\d,\d{3}) --> (\d{2}:[0-5]\d:[0-5]\d,\d{3})\n(.+)", re.S)

    def to_ms(stamp):
        h, m, s, ms = map(int, re.split(r"[:,]", stamp))
        return ((h * 60 + m) * 60 + s) * 1000 + ms

    for block in blocks:
        match = stamp_pattern.fullmatch(block.strip())
        if not match:
            continue
        idx, s_stamp, e_stamp, text = match.groups()
        cues.append({
            "idx": int(idx),
            "start_ms": to_ms(s_stamp),
            "end_ms": to_ms(e_stamp),
            "text": text.strip().replace("\n", " ")
        })
    return cues


def extract_cues_cmd(args):
    srt_text = Path(args.srt).read_text(encoding="utf-8")
    cues = parse_srt_cues(srt_text)
    candidates = []
    if not cues:
        output_json = []
    else:
        current_group = []
        seg_id = 1
        for cue in cues:
            current_group.append(cue)
            group_duration = (current_group[-1]["end_ms"] - current_group[0]["start_ms"]) / 1000.0
            if group_duration >= 15.0 or cue == cues[-1]:
                start_ms = current_group[0]["start_ms"]
                end_ms = current_group[-1]["end_ms"]
                combined_text = " ".join(c["text"] for c in current_group)
                score = 0.5
                if re.search(r"\d+|对比|但是|第一|第二|第三|首先|其次", combined_text):
                    score += 0.3
                candidates.append({
                    "segment_id": f"seg_{seg_id:03d}",
                    "cue_range": [current_group[0]["idx"], current_group[-1]["idx"]],
                    "start_ms": start_ms,
                    "end_ms": end_ms,
                    "summary_text": combined_text[:60],
                    "broll_score": round(min(score, 1.0), 2)
                })
                seg_id += 1
                current_group = []
        output_json = candidates

    output_path = Path(args.output) if args.output else Path("cue_candidates.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Extracted {len(candidates)} cue candidates -> {output_path}")


def validate_svg_cmd(args):
    svg_path = Path(args.svg)
    account = args.account.lower()
    errors, warnings = [], []

    if account not in BRAND_COLORS:
        errors.append(f"Invalid account '{account}'. Must be one of {list(BRAND_COLORS.keys())}")

    content = svg_path.read_text(encoding="utf-8")
    try:
        root = ET.fromstring(content)
    except Exception as e:
        report = {"valid": False, "account": account, "errors": [f"SVG parsing error: {e}"], "warnings": warnings}
        print(json.dumps(report, indent=2))
        return

    viewbox = root.attrib.get("viewBox", "")
    if not viewbox:
        errors.append("Missing viewBox attribute in SVG root")
    else:
        vb_parts = list(map(float, viewbox.replace(",", " ").split()))
        if len(vb_parts) == 4:
            vw, vh = vb_parts[2], vb_parts[3]
            if vw != 1080 or vh != 1920:
                warnings.append(f"viewBox dimension {vw}x{vh} is not standard 9:16 (1080x1920)")

    brand_color = BRAND_COLORS.get(account, "").upper()
    if brand_color and brand_color not in content.upper():
        errors.append(f"Brand primary color {brand_color} for '{account}' not found in SVG content")

    font_sizes = re.findall(r'font-size=["\']?(\d+)(?:px)?["\']?', content)
    for fs in font_sizes:
        if int(fs) < 28:
            errors.append(f"Font size {fs}px violates minimum requirement (>=28px)")

    valid = len(errors) == 0
    report = {"valid": valid, "account": account, "errors": errors, "warnings": warnings}
    if args.output:
        Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def render_chart_cmd(args):
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    account = config.get("account", "maxs").lower()
    brand_color = BRAND_COLORS.get(account, "#134FFF")
    motion_mode = config.get("motion_mode", "fade-in")
    step_triggers = config.get("step_triggers", [])
    title = config.get("title", "Chart Title")

    triggers_attr = json.dumps(step_triggers)
    svg_html = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" data-motion-mode="{motion_mode}" data-step-ms='{triggers_attr}'>
  <rect x="108" y="154" width="842" height="979" fill="none" stroke="{brand_color}" stroke-width="4"/>
  <text x="140" y="220" font-family="MiSans VF" font-size="48" font-weight="bold" fill="{brand_color}">{title}</text>
</svg>'''

    output_path = Path(args.output) if args.output else Path("rendered_chart.svg")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg_html, encoding="utf-8")
    print(f"Rendered declarative chart -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Pipeline Optimization Toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    cues_parser = subparsers.add_parser("extract-cues", help="Extract cue candidates")
    cues_parser.add_argument("srt", help="Input retimed SRT file")
    cues_parser.add_argument("--output", "-o", help="Output JSON file path")
    cues_parser.set_defaults(func=extract_cues_cmd)

    val_parser = subparsers.add_parser("validate-svg", help="Validate SVG compliance")
    val_parser.add_argument("svg", help="Input SVG file")
    val_parser.add_argument("--account", required=True, choices=["maxs", "jiyan", "leona"], help="Brand account")
    val_parser.add_argument("--output", "-o", help="Output JSON report file path")
    val_parser.set_defaults(func=val_parser)

    render_parser = subparsers.add_parser("render-chart", help="Render declarative chart to SVG")
    render_parser.add_argument("config", help="Input declarative chart JSON config")
    render_parser.add_argument("--output", "-o", help="Output SVG file path")
    render_parser.set_defaults(func=render_chart_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
