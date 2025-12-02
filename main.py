#!/usr/bin/env python3
"""
Generador de firmas de correo electrónico.

Este script genera firmas HTML para correo electrónico a partir de
configuraciones JSON y listas de personas en CSV.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from schemas import is_config, is_signatures_list, validate_all_rows


# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Genera firmas HTML para correo electrónico.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py                           # Modo interactivo
  python main.py -c signatures.json        # Especificar archivo de configuración
  python main.py -c config.json -p ENEM    # Seleccionar perfil por ID
  python main.py -l firmas.csv             # Especificar archivo CSV de firmas
  python main.py --preview                 # Generar índice de previsualización
        """,
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Path("signatures.json"),
        help="Archivo JSON de configuración (por defecto: signatures.json)",
    )
    parser.add_argument(
        "-p",
        "--profile",
        type=str,
        metavar="ID",
        help="Seleccionar automáticamente el perfil con el ID especificado",
    )
    parser.add_argument(
        "-l",
        "--list",
        type=Path,
        metavar="CSV",
        help="Archivo CSV con la lista de firmas (sobrescribe el valor por defecto)",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Generar un archivo index.html con todas las firmas para previsualización",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Mostrar información detallada",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Modo silencioso (solo errores)",
    )
    return parser.parse_args()


def select_config(path: Path, profile_id: str | None = None) -> dict[str, Any] | None:
    """
    Carga y selecciona una configuración del archivo JSON.

    Args:
        path: Ruta al archivo de configuración.
        profile_id: ID del perfil a seleccionar automáticamente.

    Returns:
        La configuración seleccionada o None si hay error.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            config = json.load(file)
    except FileNotFoundError:
        logger.error("No se ha encontrado el archivo %s.", path)
        return None
    except json.JSONDecodeError as e:
        logger.error("Error al parsear el archivo JSON %s: %s", path, e)
        return None
    except OSError as e:
        logger.error("Error al leer el archivo %s: %s", path, e)
        return None

    if not isinstance(config, list) or len(config) == 0:
        logger.error("No se ha encontrado ninguna configuración válida.")
        return None

    for i, c in enumerate(config):
        if not is_config(c):
            logger.error("La configuración %d no tiene el formato correcto.", i + 1)
            return None

    # Aplicar output_path por defecto si no está presente
    for c in config:
        if "output_path" not in c or not c["output_path"]:
            c["output_path"] = c["id"]

    if len(config) == 1:
        logger.info(
            "Se ha encontrado una única configuración (%s). Usándola...",
            config[0]["id"],
        )
        return config[0]

    # Selección automática por ID si se especificó
    if profile_id is not None:
        for c in config:
            if c["id"] == profile_id:
                logger.info("Usando configuración: %s", c["id"])
                return c
        available_ids = ", ".join(c["id"] for c in config)
        logger.error(
            "Perfil '%s' no encontrado. Perfiles disponibles: %s",
            profile_id,
            available_ids,
        )
        return None

    # Selección interactiva
    print(f"Se han encontrado {len(config)} configuraciones:")
    for i, c in enumerate(config):
        print(f"  {i + 1}. {c['id']}")

    try:
        input_config = input(f"Selecciona una configuración [1-{len(config)}]: ")
        index = int(input_config) - 1
        if 0 <= index < len(config):
            logger.info("Usando configuración: %s", config[index]["id"])
            return config[index]
        else:
            logger.error("Selección inválida.")
            return None
    except ValueError:
        logger.error("Selección inválida. Debe ser un número.")
        return None
    except (EOFError, KeyboardInterrupt):
        logger.info("\nOperación cancelada.")
        return None


def load_signatures_list(
    config_id: str, csv_path: Path | None = None
) -> list[list[str]] | None:
    """
    Carga la lista de firmas desde un archivo CSV.

    Args:
        config_id: ID de la configuración para construir el nombre por defecto.
        csv_path: Ruta al archivo CSV (opcional).

    Returns:
        Lista de filas del CSV o None si hay error.
    """
    default_path = Path(f"{config_id.lower()}_list.csv")

    if csv_path is None:
        try:
            path_input = input(
                f"Introduce la ruta del archivo CSV ({default_path}): "
            ).strip()
            path = Path(path_input) if path_input else default_path
        except (EOFError, KeyboardInterrupt):
            logger.info("\nOperación cancelada.")
            return None
    else:
        path = csv_path

    try:
        with open(path, newline="", encoding="utf-8") as file:
            signatures_list = list(csv.reader(file, delimiter=",", quotechar='"'))
    except FileNotFoundError:
        logger.error("No se ha encontrado el archivo %s.", path)
        return None
    except OSError as e:
        logger.error("Error al leer el archivo %s: %s", path, e)
        return None

    if not is_signatures_list(signatures_list):
        logger.error("La primera fila contiene nombres de columnas inválidos.")
        return None

    if len(signatures_list) < 2:
        logger.error(
            "La lista de firmas debe tener al menos una cabecera y una fila de datos."
        )
        return None

    # Validar filas obligatorias
    cols, errors = validate_all_rows(signatures_list)
    if errors:
        for error in errors:
            logger.error(error)
        return None

    logger.info("Se han cargado %d firmas desde %s.", len(signatures_list) - 1, path)
    return signatures_list


def validate_template(template_name: str, templates_dir: Path) -> bool:
    """
    Verifica que la plantilla especificada exista.

    Args:
        template_name: Nombre de la plantilla (sin extensión).
        templates_dir: Directorio de plantillas.

    Returns:
        True si la plantilla existe, False en caso contrario.
    """
    template_path = templates_dir / f"{template_name}.html.j2"
    if not template_path.exists():
        available = [
            p.stem
            for p in templates_dir.glob("*.html.j2")
            if not p.stem.startswith("_")
        ]
        logger.error(
            "La plantilla '%s' no existe. Plantillas disponibles: %s",
            template_name,
            ", ".join(available) or "(ninguna)",
        )
        return False
    return True


def gen_signatures(
    config: dict[str, Any],
    signatures_list: list[list[str]],
    template_name: str,
    generate_preview: bool = False,
) -> int:
    """
    Genera las firmas HTML.

    Args:
        config: Configuración de la firma.
        signatures_list: Lista de firmas a generar (incluyendo cabeceras).
        template_name: Nombre de la plantilla a usar.
        generate_preview: Si es True, genera un archivo index.html de previsualización.

    Returns:
        Número de firmas generadas.
    """
    templates_dir = Path("templates")

    if not validate_template(template_name, templates_dir):
        return 0

    template_path = f"templates/{template_name}.html.j2"
    env = Environment(loader=FileSystemLoader("."))

    try:
        template = env.get_template(template_path)
    except TemplateNotFound:
        logger.error("No se pudo cargar la plantilla %s.", template_path)
        return 0

    # Crear diccionario de columnas sin modificar la lista original
    header_row = signatures_list[0]
    cols = {value.lower().strip(): index for index, value in enumerate(header_row)}

    output_path = Path(config["output_path"])
    output_path.mkdir(parents=True, exist_ok=True)

    config["date"] = datetime.now().strftime("%Y-%m-%d")

    sign_count = 0
    generated_files: list[tuple[str, str, str]] = []  # (nombre, cargo, archivo)

    # Iterar sobre las filas de datos (sin la cabecera)
    for i, row in enumerate(signatures_list[1:]):
        local_config = config.copy()

        # Limpiar valores de cadena
        for key in local_config:
            if isinstance(local_config[key], str):
                local_config[key] = local_config[key].strip()

        # Aplicar valores del CSV
        for col, idx in cols.items():
            if idx < len(row):
                val = row[idx]
                if isinstance(val, str):
                    val = val.strip()
                    if val == "None":
                        local_config.pop(col, None)
                    elif val:
                        local_config[col] = val

        # Nombre de archivo de salida
        if "output" not in local_config or not local_config.get("output"):
            local_config["output"] = f"signature{i}"

        output_file = output_path / f"{local_config['output']}.html"
        content = template.render(local_config)
        if not content.endswith("\n"):
            content += "\n"

        try:
            with open(output_file, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            sign_count += 1
            generated_files.append(
                (
                    local_config.get("name", f"Firma {i}"),
                    local_config.get("position", ""),
                    output_file.name,
                )
            )
            logger.debug("Generada firma: %s", output_file)
        except OSError as e:
            logger.error("Error al escribir %s: %s", output_file, e)

    # Generar README.md
    if generated_files:
        readme_path = output_path / "README.md"
        readme_content = generate_readme(config, generated_files)
        try:
            with open(readme_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(readme_content)
            logger.info("Generado README: %s", readme_path)
        except OSError as e:
            logger.error("Error al escribir README: %s", e)

    # Generar índice de previsualización
    if generate_preview and generated_files:
        preview_path = output_path / "index.html"
        preview_content = generate_preview_index(config, generated_files)
        try:
            with open(preview_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(preview_content)
            logger.info("Generado índice de previsualización: %s", preview_path)
        except OSError as e:
            logger.error("Error al escribir índice de previsualización: %s", e)

    logger.info("Se han generado %d firmas en %s.", sign_count, output_path)
    return sign_count


def generate_readme(config: dict[str, Any], files: list[tuple[str, str, str]]) -> str:
    """
    Genera un archivo README.md con la lista de firmas generadas.

    Args:
        config: Configuración utilizada.
        files: Lista de tuplas (nombre, cargo, archivo).

    Returns:
        Contenido Markdown del README.
    """
    config_id = config.get("id", "Firmas")
    organization = config.get("organization", config_id)
    date = datetime.now().strftime("%Y-%m-%d")

    # Calcular anchos de columna para alineación
    max_position = max(len(position) for _, position, _ in files) if files else 5
    max_file = max(len(file) for _, _, file in files) if files else 7
    max_position = max(max_position, 5)  # Mínimo "Cargo"
    max_file = max(max_file, 7)  # Mínimo "Archivo"

    # Generar filas de la tabla con enlaces Markdown
    rows = "\n".join(
        f"| {position.ljust(max_position)} | {f'[{file}](./{file})'.ljust(max_file)} |"
        for _, position, file in files
    )

    return f"""# Firmas de {config_id}

Firmas de correo electrónico generadas automáticamente para {organization}.

**Última actualización:** {date}

## Lista de firmas

| {"Cargo".ljust(max_position)} | {"Archivo".ljust(max_file)} |
| {"-" * max_position} | {"-" * max_file} |
{rows}

## ¿Cómo usar las firmas?

Consulta las instrucciones en el [README principal](../README.md#cómo-usar-las-firmas).

---

*Generado automáticamente por [mail-signatures](https://github.com/ComicIvans/mail-signatures)*
"""


def generate_preview_index(
    config: dict[str, Any], files: list[tuple[str, str, str]]
) -> str:
    """
    Genera un archivo HTML con un índice de todas las firmas para previsualización.

    Args:
        config: Configuración utilizada.
        files: Lista de tuplas (nombre, cargo, archivo).

    Returns:
        Contenido HTML del índice.
    """
    items = "\n".join(
        f'    <li><a href="{file}" target="preview">{name} - {position}</a></li>'
        for name, position, file in files
    )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Previsualización - {config.get('id', 'Firmas')}</title>
    <style>
        body {{ font-family: system-ui, sans-serif; margin: 0; display: flex; height: 100vh; }}
        nav {{ width: 250px; padding: 20px; background: #f5f5f5; overflow-y: auto; }}
        nav h1 {{ font-size: 1.2em; margin-top: 0; }}
        nav ul {{ list-style: none; padding: 0; }}
        nav li {{ margin: 8px 0; }}
        nav a {{ color: #333; text-decoration: none; }}
        nav a:hover {{ color: {config.get('color', '#007bff')}; }}
        iframe {{ flex: 1; border: none; border-left: 1px solid #ddd; }}
    </style>
</head>
<body>
    <nav>
        <h1>{config.get('id', 'Firmas')}</h1>
        <p><small>Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}</small></p>
        <ul>
{items}
        </ul>
    </nav>
    <iframe name="preview" src="{files[0][2] if files else ''}"></iframe>
</body>
</html>
"""


def main() -> int:
    """
    Función principal del script.

    Returns:
        Código de salida (0 = éxito, 1 = error).
    """
    args = parse_args()

    # Configurar nivel de logging
    if args.quiet:
        logger.setLevel(logging.ERROR)
    elif args.verbose:
        logger.setLevel(logging.DEBUG)

    config = select_config(args.config, args.profile)
    if config is None:
        return 1

    signatures_list = load_signatures_list(config["id"], args.list)
    if signatures_list is None:
        return 1

    count = gen_signatures(
        config,
        signatures_list,
        config["template"],
        generate_preview=args.preview,
    )

    return 0 if count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
