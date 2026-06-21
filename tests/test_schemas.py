"""Tests de validación de configuración y listas de firmas."""

from __future__ import annotations

import copy

import pytest

from schemas import (
    is_config,
    is_signatures_list,
    validate_all_rows,
    validate_signature_row,
)


@pytest.fixture
def valid_config() -> dict:
    """Configuración mínima válida."""
    return {
        "id": "TEST",
        "template": "original",
        "main_font": "Montserrat",
        "name_font": "Open Sans",
        "name_image": {"image": "https://example.com/logo.png"},
        "color": "#3EB1C8",
        "organization": "Organización de prueba",
    }


# --- is_config ---------------------------------------------------------------


def test_valid_minimal_config(valid_config: dict) -> None:
    assert is_config(valid_config)


def test_valid_full_config(valid_config: dict) -> None:
    valid_config.update(
        {
            "output_path": "OUT",
            "organization_extra": "Entidad superior",
            "phone": "958 241 561",
            "phone_country_code": "+34",
            "internal_phone": "41561",
            "opt_mail": "info@example.com",
            "max_width": 315,
            "links": [
                {
                    "url": "https://example.com",
                    "image": "https://example.com/web.png",
                    "alt": "🌐",
                    "description": "Web",
                }
            ],
            "sponsor_text": "Colaboran:",
            "sponsors": [
                {"image": "https://example.com/s.png", "height": 55.55}
            ],
            "footer_address": "Calle X, 1",
            "footer_text": "<a href='https://x.es'>Legal</a>",
        }
    )
    assert is_config(valid_config)


def test_short_hex_color(valid_config: dict) -> None:
    valid_config["color"] = "#abc"
    assert is_config(valid_config)


@pytest.mark.parametrize("missing", ["id", "template", "main_font", "color", "organization"])
def test_missing_required_field(valid_config: dict, missing: str) -> None:
    del valid_config[missing]
    assert not is_config(valid_config)


def test_name_image_is_optional(valid_config: dict) -> None:
    # En la plantilla `upv` la foto puede faltar; name_image es opcional.
    del valid_config["name_image"]
    assert is_config(valid_config)


def test_unknown_key_rejected(valid_config: dict) -> None:
    valid_config["unknown_field"] = "x"
    assert not is_config(valid_config)


@pytest.mark.parametrize("color", ["red", "3EB1C8", "#GGGGGG", "#12345", ""])
def test_invalid_color(valid_config: dict, color: str) -> None:
    valid_config["color"] = color
    assert not is_config(valid_config)


def test_country_code_must_start_with_plus(valid_config: dict) -> None:
    valid_config["phone_country_code"] = "34"
    assert not is_config(valid_config)


def test_opt_mail_must_contain_at(valid_config: dict) -> None:
    valid_config["opt_mail"] = "noatsign"
    assert not is_config(valid_config)


def test_invalid_http_image_url_rejected(valid_config: dict) -> None:
    # Una URL http(s) mal formada sigue siendo inválida.
    valid_config["name_image"] = {"image": "https://"}
    assert not is_config(valid_config)


def test_local_image_path_accepted(valid_config: dict) -> None:
    # Las imágenes pueden servirse desde una ruta local relativa.
    valid_config["name_image"] = {"image": "img/logo.png"}
    assert is_config(valid_config)


@pytest.mark.parametrize("ref", ["javascript:alert(1)", "data:image/png;base64,AAAA", "file:///etc/passwd"])
def test_unsafe_image_scheme_rejected(valid_config: dict, ref: str) -> None:
    valid_config["name_image"] = {"image": ref}
    assert not is_config(valid_config)


def test_empty_required_string_rejected(valid_config: dict) -> None:
    valid_config["id"] = ""
    assert not is_config(valid_config)


@pytest.mark.parametrize("value", [0, -5])
def test_non_positive_max_width_rejected(valid_config: dict, value: int) -> None:
    valid_config["max_width"] = value
    assert not is_config(valid_config)


def test_max_width_upper_bound(valid_config: dict) -> None:
    valid_config["max_width"] = 440
    assert is_config(valid_config)
    valid_config["max_width"] = 441
    assert not is_config(valid_config)


def test_unicode_url_accepted(valid_config: dict) -> None:
    # URLs reales contienen caracteres no ASCII en la ruta (LinkedIn DGE).
    valid_config["links"] = [
        {
            "url": "https://www.linkedin.com/company/delegación-general",
            "image": "https://example.com/in.png",
        }
    ]
    assert is_config(valid_config)


# --- is_signatures_list ------------------------------------------------------


def test_valid_header() -> None:
    assert is_signatures_list([["Name", "Position", "Mail"]])


def test_header_case_insensitive_and_optional_cols() -> None:
    assert is_signatures_list([["name", "POSITION", "Mail", "Output", "Phone"]])


def test_header_missing_required_column() -> None:
    assert not is_signatures_list([["Name", "Mail"]])


def test_header_unknown_column() -> None:
    assert not is_signatures_list([["Name", "Position", "Mail", "bogus"]])


def test_empty_header() -> None:
    assert not is_signatures_list([])
    assert not is_signatures_list([[]])


# --- validate_signature_row / validate_all_rows ------------------------------


def test_row_with_all_required_values() -> None:
    cols = {"name": 0, "position": 1, "mail": 2}
    assert validate_signature_row(["Ana", "Jefa", "a@x.es"], cols, 2) == []


def test_row_with_empty_required_value_reports_line() -> None:
    cols = {"name": 0, "position": 1, "mail": 2}
    errors = validate_signature_row(["Ana", "", "a@x.es"], cols, 5)
    assert len(errors) == 1
    assert "Fila 5" in errors[0]
    assert "position" in errors[0]


def test_row_shorter_than_header() -> None:
    cols = {"name": 0, "position": 1, "mail": 2}
    errors = validate_signature_row(["Ana"], cols, 2)
    assert len(errors) == 2  # position y mail faltan


def test_validate_all_rows_collects_errors() -> None:
    data = [
        ["Name", "Position", "Mail"],
        ["Ana", "Jefa", "a@x.es"],
        ["", "Vocal", "b@x.es"],
    ]
    cols, errors = validate_all_rows(data)
    assert cols == {"name": 0, "position": 1, "mail": 2}
    assert len(errors) == 1
    assert "Fila 3" in errors[0]


def test_validate_all_rows_needs_data_row() -> None:
    cols, errors = validate_all_rows([["Name", "Position", "Mail"]])
    assert cols == {}
    assert len(errors) == 1
