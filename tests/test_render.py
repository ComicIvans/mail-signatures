"""Tests de renderizado de plantillas: escapado y HTML intencionado."""

from __future__ import annotations

import pytest
from jinja2 import Environment, FileSystemLoader


@pytest.fixture
def env() -> Environment:
    # Mismo entorno que main.gen_signatures (autoescape activado).
    return Environment(loader=FileSystemLoader("."), autoescape=True)


def base_context(**overrides) -> dict:
    ctx = {
        "date": "2026-01-01",
        "name": "Ana García",
        "position": "Presidenta",
        "organization": "Organización de prueba",
        "main_font": "Montserrat",
        "name_font": "Open Sans",
        "color": "#3EB1C8",
        "mail": "ana@example.com",
        "name_image": {"image": "https://example.com/logo.png"},
    }
    ctx.update(overrides)
    return ctx


def render(env: Environment, template: str, ctx: dict) -> str:
    return env.get_template(f"templates/{template}.html.j2").render(ctx)


@pytest.mark.parametrize("template", ["original", "wide-logo"])
def test_user_data_is_escaped(env: Environment, template: str) -> None:
    ctx = base_context(name="Tom & <b>Jerry</b>")
    out = render(env, template, ctx)
    assert "&amp;" in out
    assert "&lt;b&gt;Jerry&lt;/b&gt;" in out
    # El marcado crudo no debe colarse.
    assert "<b>Jerry</b>" not in out


@pytest.mark.parametrize("template", ["original", "wide-logo"])
def test_title_filled(env: Environment, template: str) -> None:
    out = render(env, template, base_context())
    assert "<title>Ana García - Organización de prueba</title>" in out


def test_footer_text_renders_html_unescaped(env: Environment) -> None:
    footer = "<a href='https://x.es'>Política de privacidad</a>"
    out = render(env, "original", base_context(footer_text=footer))
    assert footer in out
    assert "&lt;a href" not in out


def test_footer_address_is_escaped(env: Environment) -> None:
    # footer_address es texto plano: debe escaparse.
    out = render(env, "original", base_context(footer_address="A & B, 1"))
    assert "A &amp; B, 1" in out


def test_max_width_applied_when_present(env: Environment) -> None:
    out = render(env, "original", base_context(max_width=315))
    assert "max-width: 315px" in out


def test_max_width_absent_by_default(env: Environment) -> None:
    out = render(env, "original", base_context())
    assert "max-width:" not in out


def test_contact_info_falls_back_to_mail_only(env: Environment) -> None:
    out = render(env, "original", base_context())
    assert "mailto:ana@example.com" in out


def test_link_image_url_escaped_in_attribute(env: Environment) -> None:
    ctx = base_context(
        links=[
            {
                "url": "https://example.com/?a=1&b=2",
                "image": "https://example.com/i.png",
                "description": "Enlace",
            }
        ]
    )
    out = render(env, "original", ctx)
    assert "https://example.com/?a=1&amp;b=2" in out
