"""Schemas y validación para la configuración y lista de firmas."""

from __future__ import annotations

import re
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    ValidationError,
    field_validator,
)


# Regex para validar colores hexadecimales
HEX_COLOR_REGEX = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

# Tipos reutilizables
NonEmptyStr = Annotated[str, Field(min_length=1)]
PositiveNumber = Annotated[float, Field(gt=0)]


class _StrictModel(BaseModel):
    """Modelo base que rechaza claves desconocidas."""

    model_config = ConfigDict(extra="forbid")


class LinkModel(_StrictModel):
    url: HttpUrl
    image: HttpUrl
    alt: str | None = None
    description: str | None = None


class SponsorModel(_StrictModel):
    image: HttpUrl
    url: HttpUrl | None = None
    alt: str | None = None
    description: str | None = None
    width: PositiveNumber | None = None
    height: PositiveNumber | None = None


class NameImageModel(_StrictModel):
    image: HttpUrl
    url: HttpUrl | None = None
    alt: str | None = None
    description: str | None = None


class ConfigModel(_StrictModel):
    id: NonEmptyStr
    template: NonEmptyStr
    output_path: str | None = None
    main_font: NonEmptyStr
    name_font: NonEmptyStr
    name_image: NameImageModel
    color: str
    organization: NonEmptyStr
    organization_extra: str | None = None
    phone: str | None = None
    phone_country_code: str | None = None
    internal_phone: str | None = None
    opt_mail: str | None = None
    max_width: PositiveNumber | None = None
    links: list[LinkModel] | None = None
    sponsor_text: str | None = None
    sponsors: list[SponsorModel] | None = None
    supporter_text: str | None = None
    supporters: list[SponsorModel] | None = None
    footer_address: str | None = None
    footer_text: str | None = None

    @field_validator("color")
    @classmethod
    def _validate_color(cls, value: str) -> str:
        if not HEX_COLOR_REGEX.match(value):
            raise ValueError("debe ser un color hexadecimal válido (ej: #3EB1C8)")
        return value

    @field_validator("phone_country_code")
    @classmethod
    def _validate_country_code(cls, value: str | None) -> str | None:
        if value is not None and not value.startswith("+"):
            raise ValueError("debe empezar por '+'")
        return value

    @field_validator("opt_mail")
    @classmethod
    def _validate_opt_mail(cls, value: str | None) -> str | None:
        if value is not None and "@" not in value:
            raise ValueError("debe contener '@'")
        return value


REQ_COLUMNS_SIGNATURES_LIST: list[str] = [
    "name",
    "position",
    "mail",
]

# `name_image` se acepta como columna por compatibilidad, pero se ignora al
# generar: es un objeto en la configuración y no puede construirse desde una
# celda CSV (texto plano). Defínelo solo en `signatures.json`.
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

# Columnas que se aceptan en la cabecera pero se ignoran al aplicar overrides
# (no pueden representarse como texto plano en una celda CSV).
IGNORED_OVERRIDE_COLUMNS: frozenset[str] = frozenset({"name_image"})

_ALLOWED_COLUMNS: frozenset[str] = frozenset(
    REQ_COLUMNS_SIGNATURES_LIST + OPT_COLUMNS_SIGNATURES_LIST
)


def is_config(config: dict[str, Any]) -> bool:
    """Valida que la configuración tenga el formato correcto."""
    try:
        ConfigModel.model_validate(config)
        return True
    except ValidationError:
        return False


def is_signatures_list(signatures_list: list[list[str]]) -> bool:
    """Valida que la lista de firmas tenga el formato correcto (solo cabeceras)."""
    if not signatures_list or not signatures_list[0]:
        return False
    cols = [col.lower().strip() for col in signatures_list[0]]
    if not set(REQ_COLUMNS_SIGNATURES_LIST).issubset(cols):
        return False
    return set(cols).issubset(_ALLOWED_COLUMNS)


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
