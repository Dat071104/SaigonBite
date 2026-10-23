"""Archive actual dispatched prompts and transcripts outside the public repo."""
from pathlib import Path
import argparse
import json
import os
import zipfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-id", default=os.environ.get("CODEX_THREAD_ID"))
    args = parser.parse_args()
    if not args.session_id:
        raise SystemExit("Pass --session-id for the actual root run")
    sessions = Path(r"C:\Users\ADMIN\.codex\sessions\2026\10\23")
    matches = list(sessions.glob(f"*{args.session_id}.jsonl"))
    if len(matches) != 1:
        raise SystemExit("Expected exactly one current root transcript")
    source = matches[0]
    prompts = []
    for line in source.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        p = item.get("payload", {})
        if item.get("type") == "response_item" and p.get("type") == "function_call":
            if "spawn_agent" in p.get("name", ""):
                prompts.append({"timestamp": item.get("timestamp"), "tool": p["name"],
                                "arguments": json.loads(p["arguments"])})
    base = Path(r"D:\RAD\FINAL\Part2\notes")
    target = base / "P1_resume_prompt_archive.json"
    target.write_text(json.dumps({"source_session": source.name,
                                  "phase_prompt": r"D:\RAD\FINAL\Part2\codex\P1_PROMPT.md",
                                  "dispatched_prompts": prompts}, indent=2, ensure_ascii=False), encoding="utf-8")
    logs = [source]
    parent_ids = [args.session_id]
    prior_archive = base / "P1_prompt_archive.json"
    if prior_archive.exists():
        prior = sessions / json.loads(prior_archive.read_text(encoding="utf-8"))["source_session"]
        if prior.exists():
            logs.append(prior)
            parent_ids.append(prior.stem[-36:])
    for path in sessions.glob("*.jsonl"):
        if path in logs:
            continue
        with path.open(encoding="utf-8") as stream:
            meta = json.loads(stream.readline()).get("payload", {})
        origin = meta.get("source", {})
        if any(parent in json.dumps(origin) for parent in parent_ids):
            logs.append(path)
    with zipfile.ZipFile(base / "P1_resume_transcripts.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for path in logs:
            archive.write(path, path.name)
        for name in ("A", "B", "C", "D", "review", "root"):
            report = Path(r"D:\RAD\FINAL\SaigonBite\docs\part2\_agent_reports") / f"P1-{name}.md"
            if report.exists():
                archive.write(report, report.name)
    print("Archived dispatched prompts:", len(prompts))
    print("Archived transcripts:", len(logs))


if __name__ == "__main__":
    main()
