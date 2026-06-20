"""Tests de integración de la generación de firmas (main.gen_signatures)."""

from __future__ import annotations

from pathlib import Path

import pytest

import main


@pytest.fixture
def config(tmp_path: Path) -> dict:
    return {
        "id": "TEST",
        "template": "original",
        "output_path": str(tmp_path / "out"),
        "main_font": "Montserrat",
        "name_font": "Open Sans",
        "name_image": {"image": "https://example.com/REAL.png"},
        "color": "#3EB1C8",
        "organization": "Organización de prueba",
    }


HEADER = ["Name", "Position", "Mail", "Output"]


def test_generates_files_and_readme(config: dict) -> None:
    rows = [
        HEADER,
        ["Ana García", "Presidenta", "ana@example.com", "Firma Ana"],
        ["Juan López", "Secretario", "juan@example.com", "Firma Juan"],
    ]
    count = main.gen_signatures(config, rows, "original")
    out = Path(config["output_path"])

    assert count == 2
    assert (out / "Firma Ana.html").is_file()
    assert (out / "Firma Juan.html").is_file()
    assert (out / "README.md").is_file()
    assert "Organización de prueba" in (out / "README.md").read_text(encoding="utf-8")


def test_preview_index_created(config: dict) -> None:
    rows = [HEADER, ["Ana", "Jefa", "ana@example.com", "Firma Ana"]]
    main.gen_signatures(config, rows, "original", generate_preview=True)
    index = Path(config["output_path"]) / "index.html"
    assert index.is_file()
    assert 'iframe name="preview"' in index.read_text(encoding="utf-8")


def test_output_ends_with_newline(config: dict) -> None:
    rows = [HEADER, ["Ana", "Jefa", "ana@example.com", "Firma Ana"]]
    main.gen_signatures(config, rows, "original")
    content = (Path(config["output_path"]) / "Firma Ana.html").read_text(encoding="utf-8")
    assert content.endswith("\n")


def test_name_image_csv_column_is_ignored(config: dict) -> None:
    rows = [
        ["Name", "Position", "Mail", "Output", "name_image"],
        ["Ana", "Jefa", "ana@example.com", "Firma Ana", "JUNK_VALUE"],
    ]
    main.gen_signatures(config, rows, "original")
    content = (Path(config["output_path"]) / "Firma Ana.html").read_text(encoding="utf-8")
    assert "REAL.png" in content  # se usa el name_image de la config
    assert "JUNK_VALUE" not in content


def test_none_removes_optional_value(config: dict) -> None:
    config["phone"] = "958 241 561"
    config["phone_country_code"] = "+34"
    rows = [
        ["Name", "Position", "Mail", "Output", "phone"],
        ["Ana", "Jefa", "ana@example.com", "Firma Ana", "None"],
    ]
    main.gen_signatures(config, rows, "original")
    content = (Path(config["output_path"]) / "Firma Ana.html").read_text(encoding="utf-8")
    # Sin teléfono, contact_info cae a solo email; no debe aparecer el tel.
    assert "tel:" not in content


def test_duplicate_outputs_abort_generation(config: dict) -> None:
    rows = [
        HEADER,
        ["Ana", "Jefa", "ana@example.com", "Firma Dup"],
        ["Eva", "Vocal", "eva@example.com", "Firma Dup"],
    ]
    count = main.gen_signatures(config, rows, "original")
    assert count == 0
    assert not Path(config["output_path"]).exists() or not list(
        Path(config["output_path"]).glob("*.html")
    )


def test_unknown_template_returns_zero(config: dict) -> None:
    rows = [HEADER, ["Ana", "Jefa", "ana@example.com", "Firma Ana"]]
    assert main.gen_signatures(config, rows, "does-not-exist") == 0


# --- helpers puros -----------------------------------------------------------


def test_validate_unique_outputs_detects_duplicates() -> None:
    cols = {"name": 0, "position": 1, "mail": 2, "output": 3}
    rows = [
        ["Name", "Position", "Mail", "Output"],
        ["Ana", "Jefa", "a@x.es", "Dup"],
        ["Eva", "Vocal", "e@x.es", "Dup"],
    ]
    ok, errors = main.validate_unique_outputs(rows, cols)
    assert not ok
    assert len(errors) == 1
    assert "Dup" in errors[0]


def test_validate_unique_outputs_all_unique() -> None:
    cols = {"name": 0, "output": 1}
    rows = [["Name", "Output"], ["Ana", "A"], ["Eva", "B"]]
    ok, errors = main.validate_unique_outputs(rows, cols)
    assert ok
    assert errors == []


def test_generate_readme_lists_all_files() -> None:
    cfg = {"id": "TEST", "organization": "Org X"}
    files = [("Ana", "Jefa", "Firma Ana.html"), ("Eva", "Vocal", "Firma Eva.html")]
    md = main.generate_readme(cfg, files)
    assert "Org X" in md
    assert "[Firma Ana.html](./Firma Ana.html)" in md
    assert "Eva" in md


def test_generate_preview_index_links_all() -> None:
    cfg = {"id": "TEST", "color": "#3EB1C8"}
    files = [("Ana", "Jefa", "Firma Ana.html")]
    html = main.generate_preview_index(cfg, files)
    assert 'src="Firma Ana.html"' in html
    assert "Ana - Jefa" in html
