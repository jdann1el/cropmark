#!/usr/bin/env python3
"""Deal and record Cropmark reference-library directions. Python standard library only."""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "library"
REFS_PATH = LIBRARY / "refs.json"
DIRECTIONS_PATH = LIBRARY / "directions.json"
STYLE_DIR = ROOT / "styles"
SKILL_PATH = ROOT / "SKILL.md"
FORMATS = ("thumbnail", "post", "carousel")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
RULE_TEXT = re.compile(
    r"t-6|forced?[- ]justif|force[- ]justif|fuerza[- ]justif|forzar.{0,30}justific|"
    r"justificaci[oó]n forzada|justif\w*|stretch short phrases|wide[- ]gap examples",
    re.I,
)
REF_REQUIRED = {
    "n", "id", "title", "url", "author", "formats", "family", "role", "idea",
    "device", "hero", "type", "colour", "imagery", "measured", "tradeoffs",
    "borrow", "do_not_take", "weak_spots", "rules", "styles", "directions",
    "source", "studied", "images", "x",
}
DIRECTION_REQUIRED = {
    "id", "name", "formats", "device", "idea", "inventory_prompts", "composition",
    "needs", "styles", "seenIn", "tones", "avoid_when", "pitfalls",
    "set_continuity", "evidence",
}


def read_json(path: Path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def load_library():
    return read_json(REFS_PATH), read_json(DIRECTIONS_PATH)


def compact_text(value, limit=360):
    text = re.sub(r"\s+", " ", display_text(value)).strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def display_text(value):
    """Suppress house-rule text embedded in evidence notes; the script only deals directions."""
    text = str(value or "").strip()
    if not text:
        return ""
    text = re.sub(r"\[[^\]]*\]", "", text)
    parts = re.split(r"(?<=[.!?])\s+|;\s+", text)
    parts = [part for part in parts if not RULE_TEXT.search(part)]
    text = "; ".join(parts).strip()
    text = re.sub(r"\s+([.,;:])", r"\1", text)
    text = re.sub(r"([.,;])(?:\s*[.,;])+", r"\1", text)
    text = text.strip(" .;,")
    return text + ("." if text else "")


def first_sentences(value, count=2):
    parts = re.split(r"(?<=[.!?])\s+", str(value or "").strip())
    return " ".join(parts[:count])


def borrow_text(ref):
    borrow = ref.get("borrow", {})
    if isinstance(borrow, dict):
        return next(iter(borrow.values()), "")
    return borrow


def split_values(values):
    out = []
    for value in values or []:
        out.extend(item.strip() for item in value.split(",") if item.strip())
    return list(dict.fromkeys(out))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="validate both library JSON files")
    mode.add_argument("--show", action="store_true", help="show the saved direction record")
    mode.add_argument("--ref", metavar="ID", help="show one reference card")
    mode.add_argument("--list", choices=("directions", "refs"), help="list library entries")
    mode.add_argument("--direction", metavar="ID", help="choose and record a dealt direction")
    mode.add_argument("--redraw", choices=("direction", "style"), help="redraw one recorded choice")
    parser.add_argument("--format", choices=FORMATS)
    parser.add_argument("--brief")
    parser.add_argument("--have", action="append", default=[], metavar="ASSET[,ASSET]")
    parser.add_argument("--keep", action="append", default=[], metavar="FIELD[,FIELD]")
    parser.add_argument("--tone")
    parser.add_argument("--avoid", action="append", default=[], metavar="ID[,ID]")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--options", type=int, choices=(3,), help="deal three candidate directions")
    parser.add_argument("--why", help="reason for choosing --direction")
    parser.add_argument("--reason", help="required reason for --redraw")
    args = parser.parse_args(argv)
    if args.direction and not args.why:
        parser.error("--direction requires --why")
    if args.redraw and not args.reason:
        parser.error("--redraw requires --reason")
    if not any((args.check, args.show, args.ref, args.list, args.redraw)):
        if not args.format or args.brief is None:
            parser.error("a draw requires --format and --brief")
    return args


def normalize_input(args):
    brief = args.brief or ""
    brief_path = Path(brief).expanduser()
    brief_text = brief_path.read_text(encoding="utf-8") if brief and brief_path.is_file() else brief
    return {
        "format": args.format,
        "brief": brief,
        "brief_text": brief_text,
        "have": split_values(args.have),
        "keep": split_values(args.keep),
        "tone": args.tone,
        "avoid": split_values(args.avoid),
    }


def read_history():
    path = Path(os.environ.get("CROPMARK_HISTORY", str(Path.home() / ".cropmark" / "history.json"))).expanduser()
    try:
        data = read_json(path)
    except (OSError, json.JSONDecodeError):
        return path, []
    if isinstance(data, list):
        picks = data
    elif isinstance(data, dict):
        picks = data.get("picks", [])
    else:
        picks = []
    return path, [p for p in picks if isinstance(p, dict)]


def append_history(direction_id, style_id, seed):
    path, picks = read_history()
    entry = {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "direction": direction_id,
        "style": style_id,
        "seed": seed,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"picks": [entry] + picks[:23]}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def recent_direction_ids(picks):
    out = []
    for item in picks[:5]:
        value = item.get("direction") or item.get("id")
        if value:
            out.append(value)
    return out


def candidate_pool(directions, input_data):
    format_pool = [d for d in directions if input_data["format"] in d.get("formats", [])]
    candidates = [
        d for d in directions
        if input_data["format"] in d.get("formats", []) and d["id"] not in input_data["avoid"]
    ]
    notes = []
    if len(candidates) < 3 and len(format_pool) >= 3:
        candidates = format_pool
        notes.append("Widened the explicit avoid filter because it left fewer than 3 directions for this format.")
    if not candidates:
        raise ValueError(f"No directions are available for format {input_data['format']}.")
    have = set(input_data["have"])

    def feasible(direction):
        needs = direction.get("needs", ["none"])
        return "none" in needs or all(need in have for need in needs)

    feasible_pool = [d for d in candidates if feasible(d)]
    pool = feasible_pool
    if input_data["tone"] and len(feasible_pool) >= 3:
        toned = [d for d in feasible_pool if input_data["tone"] in d.get("tones", [])]
        if len(toned) >= 3:
            pool = toned
        else:
            notes.append(f"Tone filter left {len(toned)} matching directions; retained the feasible pool.")
    if len(pool) < 3:
        pool = candidates
        notes.append(
            f"Widened from {len(feasible_pool)} asset-feasible direction(s) to {len(candidates)} format-matching direction(s) because fewer than 3 were available."
        )
    return pool, feasible_pool, notes


def deal_options(directions, input_data, seed, picks):
    pool, feasible_pool, notes = candidate_pool(directions, input_data)
    recent = set(recent_direction_ids(picks))
    fresh = [d for d in pool if d["id"] not in recent]
    if len(fresh) >= 3:
        deal_pool = fresh
    else:
        deal_pool = pool
        if recent:
            notes.append("Fewer than 3 fresh directions remained; recent picks were allowed to fill the deal.")
    rng = random.Random(seed)
    if len(deal_pool) >= 3:
        options = rng.sample(deal_pool, 3)
    else:
        options = rng.sample(deal_pool, len(deal_pool))
        notes.append(f"Only {len(options)} direction(s) remain after format and avoid filters.")
    return options, pool, feasible_pool, notes


def option_refs(direction, refs):
    by_id = {r["id"]: r for r in refs}
    linked = [by_id[rid] for rid in direction.get("seenIn", []) if rid in by_id]
    linked.sort(key=lambda r: (r.get("role") != "exemplar", r.get("role") != "mixed", r.get("id")))
    chosen = list(linked[:2])
    if len(chosen) < 2:
        context = [
            r for r in refs
            if direction.get("formats") and set(r.get("formats", [])) & set(direction["formats"])
            and r not in chosen
        ]
        context.sort(key=lambda r: (r.get("role") != "exemplar", r.get("role") != "mixed", r.get("id")))
        chosen.extend(context[: 2 - len(chosen)])
    return [(r, r["id"] in direction.get("seenIn", [])) for r in chosen]


def print_ref_line(ref, linked):
    tag = "evidence" if linked else "context only; not linked evidence"
    print(f"  - {ref['id']} ({ref.get('role', 'reference')}; {tag}) · {compact_text(ref.get('idea'))} · Borrow: {compact_text(borrow_text(ref), 180)}")


def print_options(options, refs, input_data, seed, notes):
    print(f"Seed: {seed}")
    for note in notes:
        print(f"Note: {note}")
    print(f"Format: {input_data['format']} · Have: {', '.join(input_data['have']) or 'none'}")
    if input_data["keep"]:
        print(f"Keep: {', '.join(input_data['keep'])}")
    if input_data["tone"]:
        print(f"Tone: {input_data['tone']}")
    print("Choose the direction that carries an item from the subject inventory; record why with --direction <id> --why '…'.\n")
    for index, direction in enumerate(options, 1):
        composition = direction.get("composition", {}).get(input_data["format"], "not studied — compose from formats/" + input_data["format"] + ".md")
        print(f"{index}. {direction['id']} — {direction['name']}")
        print(f"   Idea: {compact_text(first_sentences(direction.get('idea')), 320)}")
        print(f"   Composition: {compact_text(composition, 300)}")
        print(f"   Needs: {', '.join(direction.get('needs', ['none']))}")
        print(f"   Evidence: {compact_text(direction.get('evidence'), 260)}")
        print("   Reference summaries:")
        for ref, linked in option_refs(direction, refs):
            print_ref_line(ref, linked)
        if not option_refs(direction, refs):
            print("  - No available reference summaries.")
        print()


def draw_paths():
    state_dir = Path.cwd() / ".cropmark"
    return state_dir, state_dir / "last-draw.json", state_dir / "direction.json"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def comparable_input(a, b):
    if not isinstance(a, dict) or not isinstance(b, dict):
        return False
    keys = ("format", "brief", "have", "keep", "tone", "avoid")
    return all(a.get(k) == b.get(k) for k in keys)


def output_deal(args, refs, directions, input_data, options_path):
    _, picks = read_history()
    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(1, 2**31)
    options, pool, feasible_pool, notes = deal_options(directions, input_data, seed, picks)
    record = {
        "version": 1,
        "input": input_data,
        "seed": seed,
        "dealt_options": [d["id"] for d in options],
        "notes": notes,
    }
    write_json(options_path, record)
    print_options(options, refs, input_data, seed, notes)
    return record, pool


def precedence_line():
    for line in SKILL_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("Precedence when modules disagree:"):
            return line
    raise ValueError("SKILL.md is missing its precedence line")


def print_direction_sheet(state, refs, directions):
    chosen = state["choice"]
    direction = next(d for d in directions if d["id"] == chosen["direction"])
    print(f"Direction: {direction['id']} — {direction['name']}")
    print(f"Seed: {state['seed']} · reason: {state['reason']}")
    for note in state.get("deal_notes", []):
        print(f"Note: {note}")
    if state["input"].get("keep"):
        print(f"Keep: {', '.join(state['input']['keep'])}")
    if state["input"].get("tone"):
        print(f"Tone: {state['input']['tone']}")
    print(f"Idea: {display_text(direction['idea'])}")
    fmt = state["input"]["format"]
    composition = direction.get("composition", {}).get(fmt, f"not studied — compose from formats/{fmt}.md")
    print(f"Composition ({fmt}): {display_text(composition)}")
    print(f"Needs: {', '.join(direction.get('needs', ['none']))}")
    print(f"Evidence: {display_text(direction.get('evidence', ''))}")
    print(f"Styles: {', '.join(direction.get('styles', []))}")
    print(f"Selected style: {chosen['style']} (redraw with --redraw style --reason '…' if needed)")
    ref_by_id = {r["id"]: r for r in refs}
    linked = [ref_by_id[rid] for rid in direction.get("seenIn", []) if rid in ref_by_id]
    linked.sort(key=lambda r: (r.get("role") != "exemplar", r.get("role") != "mixed", r.get("id")))
    if not linked:
        print("References: none studied for this direction.")
    for ref in linked[:3]:
        print(f"Reference {ref['id']} — {ref['title']}")
        print(f"  Idea: {compact_text(ref.get('idea'))}")
        print(f"  Hero: {compact_text(ref.get('hero'))}")
        print(f"  Borrow: {compact_text(borrow_text(ref))}")
        print(f"  Do not take: {compact_text('; '.join(ref.get('do_not_take', [])))}")
        print(f"  Weak spots: {compact_text('; '.join(ref.get('weak_spots', [])) or 'none recorded')}")
        cache_path = ROOT.parents[1] / "refs-cache" / ref["id"]
        print(f"  Local images: refs-cache/{ref['id']}/ {'present' if cache_path.is_dir() and any(cache_path.iterdir()) else 'absent'}")
    print(precedence_line())
    print("Use the selected existing style card to compose; the direction sheet records the choice and reason.")


def handle_direction(args, refs_doc, directions_doc, input_data, options_path, state_path):
    refs, directions = refs_doc["refs"], directions_doc["directions"]
    direction = next((d for d in directions if d["id"] == args.direction), None)
    if direction is None:
        raise ValueError(f"Unknown direction {args.direction!r}.")
    if input_data["format"] not in direction.get("formats", []):
        raise ValueError(f"Direction {args.direction!r} is not available for {input_data['format']}.")
    _, history = read_history()
    cached = None
    if options_path.exists():
        try:
            cached = read_json(options_path)
        except (OSError, json.JSONDecodeError):
            cached = None
    if cached and comparable_input(cached.get("input"), input_data):
        seed = cached.get("seed")
        dealt = cached.get("dealt_options", [])
        deal_notes = cached.get("notes", [])
    else:
        seed = args.seed if args.seed is not None else random.SystemRandom().randrange(1, 2**31)
        options, _, _, notes = deal_options(directions, input_data, seed, history)
        dealt = [d["id"] for d in options]
        deal_notes = notes
        print_options(options, refs, input_data, seed, notes)
    # A direct selection remains valid if it satisfies the format and avoid filters.
    if args.direction in input_data["avoid"]:
        raise ValueError("The selected direction is listed in --avoid.")
    eligible, feasible, fresh_notes = candidate_pool(directions, input_data)
    if direction not in eligible:
        raise ValueError(f"Direction {args.direction!r} does not meet the available-asset filter.")
    if args.direction not in feasible and not deal_notes:
        deal_notes = fresh_notes
    if args.direction not in dealt:
        dealt = (dealt + [args.direction])[-3:]
    styles = direction.get("styles", [])
    if not styles:
        raise ValueError(f"Direction {args.direction!r} has no style card.")
    style = random.Random(seed ^ 0xC20F4A).choice(styles)
    state = {
        "version": 1,
        "input": input_data,
        "seed": seed,
        "dealt_options": dealt,
        "deal_notes": deal_notes,
        "choice": {"direction": args.direction, "style": style},
        "reason": args.why,
        "redraw_count": 0,
        "redraw_reasons": [],
    }
    write_json(state_path, state)
    write_json(options_path, {"version": 1, "input": input_data, "seed": seed, "dealt_options": dealt, "notes": deal_notes})
    append_history(args.direction, style, seed)
    print_direction_sheet(state, refs, directions)


def handle_redraw(args, refs_doc, directions_doc, state_path):
    if not state_path.exists():
        raise ValueError("No saved direction; run --direction first.")
    state = read_json(state_path)
    directions = directions_doc["directions"]
    old_choice = state["choice"].copy()
    seed = int(state["seed"]) + int(state.get("redraw_count", 0)) + 1
    if args.redraw == "style":
        direction = next(d for d in directions if d["id"] == old_choice["direction"])
        pool = [style for style in direction.get("styles", []) if style != old_choice["style"]]
        if not pool:
            raise ValueError("This direction has no alternate style to redraw.")
        new_style = random.Random(seed).choice(pool)
        state["choice"]["style"] = new_style
        observed = {"slot": "style", "before": old_choice["style"], "after": new_style}
    else:
        input_data = state["input"]
        input_data = dict(input_data)
        input_data["avoid"] = list(dict.fromkeys(input_data.get("avoid", []) + [old_choice["direction"]]))
        _, picks = read_history()
        options, pool, _, notes = deal_options(directions, input_data, seed, picks)
        if not options:
            raise ValueError("No alternate direction can be dealt for this format.")
        new_direction = options[0]
        if not new_direction.get("styles"):
            raise ValueError("The replacement direction has no style card.")
        new_style = random.Random(seed ^ 0xC20F4A).choice(new_direction["styles"])
        state["choice"] = {"direction": new_direction["id"], "style": new_style}
        observed = {
            "slot": "direction", "before": old_choice["direction"],
            "after": new_direction["id"], "seed": seed,
            "dealt_options": [d["id"] for d in options], "notes": notes,
        }
    state["redraw_count"] = int(state.get("redraw_count", 0)) + 1
    state.setdefault("redraw_reasons", []).append({"reason": args.reason, **observed})
    write_json(state_path, state)
    if args.redraw == "direction":
        append_history(state["choice"]["direction"], state["choice"]["style"], seed)
    print_direction_sheet(state, refs_doc["refs"], directions)


def list_entries(kind, fmt, refs_doc, directions_doc):
    if kind == "directions":
        items = directions_doc["directions"]
        if fmt:
            items = [d for d in items if fmt in d.get("formats", [])]
        for item in items:
            print(f"{item['id']} · {item['name']} · {', '.join(item.get('formats', []))} · needs {', '.join(item.get('needs', ['none']))}")
    else:
        items = refs_doc["refs"]
        if fmt:
            items = [r for r in items if fmt in r.get("formats", [])]
        for item in items:
            print(f"{item['id']} · {item['title']} · {', '.join(item.get('formats', []))} · {item.get('role', '')}")


def print_ref(ref):
    # The card's source metadata is useful; its private selection weight is not a score to display.
    visible = {key: value for key, value in ref.items() if key not in ("weight", "rules")}
    for key, value in list(visible.items()):
        if isinstance(value, str):
            visible[key] = display_text(value)
        elif isinstance(value, list):
            visible[key] = [display_text(item) if isinstance(item, str) else item for item in value]
        elif isinstance(value, dict):
            visible[key] = {subkey: display_text(item) if isinstance(item, str) else item for subkey, item in value.items()}
    print(json.dumps(visible, indent=2, ensure_ascii=False))


def walk_strings(value, path="$", key=None):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from walk_strings(child, f"{path}.{child_key}", child_key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_strings(child, f"{path}[{index}]", key)
    elif isinstance(value, str):
        yield path, key, value


def is_image_or_cdn_url(value):
    parsed = urlsplit(value.rstrip(".,;:!?)\"'"))
    if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc:
        return False
    host = parsed.hostname.lower() if parsed.hostname else ""
    path = parsed.path.lower()
    suffix = Path(path.split("?", 1)[0]).suffix
    return "cdn" in host or suffix in IMAGE_SUFFIXES or any(part == "project_modules" for part in path.split("/"))


def check_library(refs_doc=None, directions_doc=None):
    errors = []
    try:
        refs_doc = refs_doc if refs_doc is not None else read_json(REFS_PATH)
        directions_doc = directions_doc if directions_doc is not None else read_json(DIRECTIONS_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load library JSON: {exc}"]
    if not isinstance(refs_doc, dict) or not isinstance(refs_doc.get("refs"), list):
        return ["refs.json must be an object with a refs array"]
    if not isinstance(directions_doc, dict) or not isinstance(directions_doc.get("directions"), list):
        return ["directions.json must be an object with a directions array"]
    for label, document, fields in (
        ("refs.json", refs_doc, ("version", "studied", "source_note", "refs")),
        ("directions.json", directions_doc, ("version", "directions")),
    ):
        missing_root = [field for field in fields if field not in document]
        if missing_root:
            errors.append(f"{label} missing required root fields: {', '.join(missing_root)}")
    refs = refs_doc["refs"]
    directions = directions_doc["directions"]
    ref_ids = [r.get("id") for r in refs if isinstance(r, dict)]
    direction_ids = [d.get("id") for d in directions if isinstance(d, dict)]
    if len(ref_ids) != len(set(ref_ids)):
        errors.append("reference ids must be unique")
    if len(direction_ids) != len(set(direction_ids)):
        errors.append("direction ids must be unique")
    refs_by_id = {r.get("id"): r for r in refs if isinstance(r, dict)}
    directions_by_id = {d.get("id"): d for d in directions if isinstance(d, dict)}
    for index, ref in enumerate(refs):
        if not isinstance(ref, dict):
            errors.append(f"refs[{index}] must be an object")
            continue
        missing = sorted(REF_REQUIRED - set(ref))
        if missing:
            errors.append(f"refs[{index}] missing required fields: {', '.join(missing)}")
        for field in ("formats", "measured", "tradeoffs", "do_not_take", "weak_spots", "rules", "styles", "directions"):
            if field in ref and not isinstance(ref[field], list):
                errors.append(f"refs[{index}].{field} must be an array")
        if "author" in ref and ref["author"] is not None and not isinstance(ref["author"], str):
            errors.append(f"refs[{index}].author must be a string or null")
        if not isinstance(ref.get("images"), dict) or ref.get("images", {}).get("committed") is not False:
            errors.append(f"refs[{index}].images must be an object with committed=false")
        for path, key, value in walk_strings(ref.get("images", {}), f"refs[{index}].images"):
            if re.search(r"https?://", value, re.I):
                errors.append(f"HTTP URL in {path}")
        for direction_id in ref.get("directions", []):
            direction = directions_by_id.get(direction_id)
            if direction is None:
                errors.append(f"reference {ref.get('id')} links to unknown direction {direction_id}")
            elif ref.get("id") not in direction.get("seenIn", []):
                errors.append(f"reference/direction link is not reciprocal: {ref.get('id')} ↔ {direction_id}")
        for style_id in ref.get("styles", []):
            if not (STYLE_DIR / f"{style_id}.md").is_file():
                errors.append(f"reference {ref.get('id')} uses missing style file {style_id}.md")
    for index, direction in enumerate(directions):
        if not isinstance(direction, dict):
            errors.append(f"directions[{index}] must be an object")
            continue
        missing = sorted(DIRECTION_REQUIRED - set(direction))
        if missing:
            errors.append(f"directions[{index}] missing required fields: {', '.join(missing)}")
        for field in ("formats", "inventory_prompts", "needs", "styles", "seenIn", "tones"):
            if field in direction and not isinstance(direction[field], list):
                errors.append(f"directions[{index}].{field} must be an array")
        composition = direction.get("composition")
        if not isinstance(composition, dict):
            errors.append(f"directions[{index}].composition must be an object")
        else:
            for fmt in direction.get("formats", []):
                if not isinstance(composition.get(fmt), str) or not composition[fmt].strip():
                    errors.append(f"direction {direction.get('id')} needs composition text for {fmt}")
        for ref_id in direction.get("seenIn", []):
            ref = refs_by_id.get(ref_id)
            if ref is None:
                errors.append(f"direction {direction.get('id')} links to unknown reference {ref_id}")
            elif direction.get("id") not in ref.get("directions", []):
                errors.append(f"direction/reference link is not reciprocal: {direction.get('id')} ↔ {ref_id}")
        for style_id in direction.get("styles", []):
            if not (STYLE_DIR / f"{style_id}.md").is_file():
                errors.append(f"direction {direction.get('id')} uses missing style file {style_id}.md")
    for fmt in FORMATS:
        count = sum(1 for d in directions if isinstance(d, dict) and fmt in d.get("formats", []))
        if count < 5:
            errors.append(f"format {fmt} has {count} directions; at least 5 required")
    # Scan every card string, including prose fields, for direct image/CDN URLs.
    for doc_name, document in (("refs.json", refs_doc), ("directions.json", directions_doc)):
        for path, key, value in walk_strings(document):
            for match in re.findall(r"https?://[^\s\"'<>]+", value, flags=re.I):
                if is_image_or_cdn_url(match):
                    errors.append(f"image or CDN URL found in {doc_name}:{path}")
    return errors


def main(argv=None):
    args = parse_args(argv)
    try:
        refs_doc, directions_doc = load_library()
        if args.check:
            errors = check_library(refs_doc, directions_doc)
            if errors:
                print("Library check failed:", file=sys.stderr)
                for error in errors:
                    print(f"- {error}", file=sys.stderr)
                return 1
            print(f"Library check passed: {len(refs_doc['refs'])} refs, {len(directions_doc['directions'])} directions.")
            return 0
        if args.show:
            _, _, state_path = draw_paths()
            if not state_path.exists():
                raise ValueError("No saved direction at .cropmark/direction.json.")
            print(json.dumps(read_json(state_path), indent=2, ensure_ascii=False))
            return 0
        if args.ref:
            ref = next((r for r in refs_doc["refs"] if r["id"] == args.ref), None)
            if ref is None:
                raise ValueError(f"Unknown reference {args.ref!r}.")
            print_ref(ref)
            return 0
        if args.list:
            list_entries(args.list, args.format, refs_doc, directions_doc)
            return 0
        _, options_path, state_path = draw_paths()
        if args.redraw:
            handle_redraw(args, refs_doc, directions_doc, state_path)
            return 0
        input_data = normalize_input(args)
        if args.direction:
            handle_direction(args, refs_doc, directions_doc, input_data, options_path, state_path)
            return 0
        output_deal(args, refs_doc["refs"], directions_doc["directions"], input_data, options_path)
        return 0
    except (OSError, ValueError, json.JSONDecodeError, StopIteration) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
