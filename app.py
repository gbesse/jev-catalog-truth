"""Review Backstage Component metadata changes against a README excerpt."""

import argparse
import json
import os
from pathlib import Path
import sys

import yaml

from jev import evaluate, normalize
from review_core import InputError, review


def component(source):
    if not isinstance(source, str) or len(source) > 50_000:
        raise InputError("invalid_yaml")
    try:
        entity = yaml.safe_load(source)
    except yaml.YAMLError as exc:
        raise InputError("invalid_yaml") from exc
    if (
        not isinstance(entity, dict)
        or entity.get("apiVersion") != "backstage.io/v1alpha1"
        or entity.get("kind") != "Component"
    ):
        raise InputError("unsupported_entity")
    metadata, spec = entity.get("metadata"), entity.get("spec")
    if not isinstance(metadata, dict) or not isinstance(spec, dict):
        raise InputError("invalid_entity")
    values = {
        "name": metadata.get("name"),
        "description": metadata.get("description", ""),
        "type": spec.get("type"),
        "lifecycle": spec.get("lifecycle"),
        "owner": spec.get("owner"),
    }
    if any(
        not isinstance(value, str) or len(value) > 1000 for value in values.values()
    ):
        raise InputError("invalid_entity")
    if any(not values[key] for key in ("name", "type", "lifecycle", "owner")):
        raise InputError("invalid_entity")
    return values


def adapt(payload):
    if not isinstance(payload, dict):
        raise InputError("invalid_case")
    before = component(payload.get("before_yaml"))
    after = component(payload.get("after_yaml"))
    if before["name"] != after["name"]:
        raise InputError("entity_mismatch")
    readme, reason = payload.get("readme_excerpt"), payload.get("reason")
    if (
        not isinstance(readme, str)
        or not 1 <= len(readme.strip()) <= 4000
        or not isinstance(reason, str)
        or not 1 <= len(reason.strip()) <= 1000
    ):
        raise InputError("invalid_context")
    changes = [
        {"field": key, "before": before[key], "after": after[key]}
        for key in ("description", "type", "lifecycle", "owner")
        if before[key] != after[key]
    ]
    if not changes:
        raise InputError("no_changes")
    flags = []
    if before["owner"] != after["owner"]:
        flags.append("owner_changed")
    if before["lifecycle"] != after["lifecycle"]:
        flags.append("lifecycle_changed")
    text = (
        "Change reason: "
        + reason.strip()
        + "\nBackstage Component: "
        + after["name"]
        + "\nMetadata changes: "
        + json.dumps(changes, sort_keys=True)
        + "\nREADME excerpt: "
        + readme.strip()
    )
    return {
        "subject": after["name"],
        "text": text,
        "evidence": ["before_yaml", "after_yaml", "readme_excerpt"],
        "flags": flags,
    }


def load_example():
    return {
        "before_yaml": Path("examples/before.yaml").read_text(encoding="utf-8"),
        "after_yaml": Path("examples/after.yaml").read_text(encoding="utf-8"),
        "readme_excerpt": Path("examples/README-excerpt.txt").read_text(
            encoding="utf-8"
        ),
        "reason": "Routine metadata cleanup",
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true")
    mode.add_argument("--input", type=Path)
    mode.add_argument("--before", type=Path)
    parser.add_argument("--after", type=Path)
    parser.add_argument("--readme", type=Path)
    parser.add_argument("--reason")
    args = parser.parse_args()
    try:
        with open("examples/policy.json", encoding="utf-8") as source:
            policy = json.load(source)
        if args.demo:
            payload = load_example()
            judge = lambda _: normalize("contradiction", 0.97, policy)
        else:
            if args.input:
                if str(args.input) == "-":
                    raw = sys.stdin.buffer.read(100_001)
                    if len(raw) > 100_000:
                        raise InputError("input_too_large")
                    payload = json.loads(raw)
                else:
                    if args.input.stat().st_size > 100_000:
                        raise InputError("input_too_large")
                    with args.input.open(encoding="utf-8") as source:
                        payload = json.load(source)
            else:
                if not args.after or not args.readme or not args.reason:
                    raise InputError("missing_files")
                if any(
                    path.stat().st_size > 50_000
                    for path in (args.before, args.after, args.readme)
                ):
                    raise InputError("input_too_large")
                payload = {
                    "before_yaml": args.before.read_text(encoding="utf-8"),
                    "after_yaml": args.after.read_text(encoding="utf-8"),
                    "readme_excerpt": args.readme.read_text(encoding="utf-8"),
                    "reason": args.reason,
                }
            key = os.environ.get("TYPESAFE_API_KEY")
            if not key:
                raise InputError("missing_key")
            judge = lambda text: evaluate(text, policy, key)
        result = review(payload, policy, judge, adapt)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        code = str(exc) if isinstance(exc, InputError) else "invalid_input"
        parser.exit(2, code + "\n")
    except Exception:
        parser.exit(3, "decision_unavailable\n")
    result["demo"] = args.demo
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
