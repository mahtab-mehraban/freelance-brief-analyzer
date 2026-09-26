import json

from brief_analyzer.cli import main


def test_cli_writes_json_output(tmp_path, capsys) -> None:
    output_path = tmp_path / "analysis.json"

    exit_code = main(
        [
            "--client",
            "Acme",
            "--brief",
            "Create a secure FastAPI API with PostgreSQL.",
            "--output",
            str(output_path),
        ]
    )

    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert saved["client"] == "Acme"
    assert "Backend API" in saved["technologies"]
    assert "Saved JSON analysis" in capsys.readouterr().out
