"""Schemas y validación para la configuración y lista de firmas."""

import re
from typing import Any

from schema import Schema, Optional, And, Or, SchemaError, Regex


# Regex para validar colores hexadecimales
HEX_COLOR_REGEX = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

# Regex para validar URLs (básica)
URL_REGEX = re.compile(
    r"^https?://"  # http:// o https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # dominio
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # IP
    r"(?::\d+)?"  # puerto opcional
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def is_hex_color(value: str) -> bool:
    """Valida que el valor sea un color hexadecimal válido."""
    return bool(HEX_COLOR_REGEX.match(value))


def is_url(value: str) -> bool:
    """Valida que el valor sea una URL válida."""
    return bool(URL_REGEX.match(value))


S_LINK = Schema(
    {
        "url": And(str, is_url),
        "image": And(str, is_url),
        Optional("alt"): str,
        Optional("description"): str,
    }
)

S_SPONSOR = Schema(
    {
        Optional("url"): And(str, is_url),
        "image": And(str, is_url),
        Optional("alt"): str,
        Optional("description"): str,
        Optional("width"): And(Or(int, float), lambda x: x > 0),
        Optional("height"): And(Or(int, float), lambda x: x > 0),
    }
)

S_NAME_IMAGE = Schema(
    Or(
        And(str, is_url),  # Retrocompatibilidad: solo URL string
        {  # Nuevo formato: objeto con propiedades
            "image": And(str, is_url),
            Optional("url"): And(str, is_url),
            Optional("alt"): str,
            Optional("description"): str,
        },
    )
)

S_CONFIG = Schema(
    {
        "id": And(str, len),
        "template": And(str, len),
        Optional("output_path"): str,
        "main_font": And(str, len),
        "name_font": And(str, len),
        "name_image": S_NAME_IMAGE,
        "color": And(str, is_hex_color),
        "organization": And(str, len),
        Optional("organization_extra"): str,
        Optional("phone"): str,
        Optional("phone_country_code"): And(str, lambda x: x.startswith("+")),
        Optional("internal_phone"): str,
        Optional("opt_mail"): And(str, lambda x: "@" in x),
        Optional("max_width"): And(Or(int, float), lambda x: x > 0),
        Optional("links"): [S_LINK],
        Optional("sponsor_text"): str,
        Optional("sponsors"): [S_SPONSOR],
        Optional("supporter_text"): str,
        Optional("supporters"): [S_SPONSOR],
        Optional("footer_address"): str,
        Optional("footer_text"): str,
    }
)

REQ_COLUMNS_SIGNATURES_LIST: list[str] = [
    "name",
    "position",
    "mail",
]

OPT_COLUMNS_SIGNATURES_LIST: list[str] = [
    "output",
    "phone",
    "phone_country_code",
    "internal_phone",
    "opt_mail",
    "organization_extra",
    "main_font",
    "name_font",
    "max_width",
    "name_image",
    "color",
    "organization",
]

S_SIGNATURES_LIST = Schema(
    And(
        REQ_COLUMNS_SIGNATURES_LIST + OPT_COLUMNS_SIGNATURES_LIST,
        lambda cols: set(REQ_COLUMNS_SIGNATURES_LIST).issubset(set(cols)),
    )
)


def is_config(config: dict[str, Any]) -> bool:
    """Valida que la configuración tenga el formato correcto."""
    try:
        S_CONFIG.validate(config)
        return True
    except SchemaError:
        return False


def is_signatures_list(signatures_list: list[list[str]]) -> bool:
    """Valida que la lista de firmas tenga el formato correcto (solo cabeceras)."""
    if not signatures_list or not signatures_list[0]:
        return False
    cols = [col.lower().strip() for col in signatures_list[0]]
    try:
        S_SIGNATURES_LIST.validate(cols)
        return True
    except SchemaError:
        return False


def validate_signature_row(
    row: list[str], cols: dict[str, int], row_number: int
) -> list[str]:
    """
    Valida que una fila tenga valores en las columnas obligatorias.

    Args:
        row: La fila de datos.
        cols: Diccionario con nombres de columnas y sus índices.
        row_number: Número de fila para mensajes de error.

    Returns:
        Lista de errores encontrados (vacía si no hay errores).
    """
    errors: list[str] = []
    for req_col in REQ_COLUMNS_SIGNATURES_LIST:
        if req_col in cols:
            idx = cols[req_col]
            if idx >= len(row) or not row[idx].strip():
                errors.append(
                    f"Fila {row_number}: la columna obligatoria '{req_col}' está vacía."
                )
    return errors


def validate_all_rows(
    signatures_list: list[list[str]],
) -> tuple[dict[str, int], list[str]]:
    """
    Valida todas las filas de la lista de firmas.

    Args:
        signatures_list: Lista completa incluyendo cabeceras.

    Returns:
        Tupla con (diccionario de columnas, lista de errores).
    """
    if len(signatures_list) < 2:
        return {}, ["La lista debe tener al menos una cabecera y una fila de datos."]

    cols = {
        value.lower().strip(): index for index, value in enumerate(signatures_list[0])
    }

    all_errors: list[str] = []
    for i, row in enumerate(signatures_list[1:], start=2):
        errors = validate_signature_row(row, cols, i)
        all_errors.extend(errors)

    return cols, all_errors
