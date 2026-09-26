"""Command-line interface for the freelance brief analyzer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .analyzer import BriefAnalysis, analyze_brief


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Turn a freelance project brief into a delivery checklist."
    )
    parser.add_argument("--client", help="Client or company name")
    parser.add_argument("--brief", help="Project brief as text")
    parser.add_argument("--brief-file", type=Path, help="UTF-8 text file containing the brief")
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional JSON file path for the structured analysis",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the program and return a terminal-friendly exit code."""
    args = build_parser().parse_args(argv)
    client = args.client or input("Client name: ").strip()
    brief = _read_brief(args)

    try:
        analysis = analyze_brief(client, brief)
    except ValueError as error:
        print(f"Error: {error}")
        return 2

    print(_format_analysis(analysis))
    if args.output:
        _write_output(args.output, analysis)
        print(f"\nSaved JSON analysis to: {args.output}")
    return 0


def _read_brief(args: argparse.Namespace) -> str:
    if args.brief and args.brief_file:
        raise SystemExit("Use either --brief or --brief-file, not both.")
    if args.brief_file:
        try:
            return args.brief_file.read_text(encoding="utf-8")
        except OSError as error:
            raise SystemExit(f"Could not read brief file: {error}") from error
    return args.brief or input("Project brief: ").strip()


def _write_output(path: Path, analysis: BriefAnalysis) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(analysis.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _format_analysis(analysis: BriefAnalysis) -> str:
    def bullet_list(items: list[str]) -> str:
        return "\n".join(f"  - {item}" for item in items)

    return (
        f"\nClient: {analysis.client}\n"
        f"Summary: {analysis.summary}\n\n"
        f"Likely work areas:\n{bullet_list(analysis.technologies)}\n\n"
        f"Delivery risks:\n{bullet_list(analysis.risks)}\n\n"
        f"Questions for discovery:\n{bullet_list(analysis.discovery_questions)}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
