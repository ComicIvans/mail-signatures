# Generador de firmas para el correo

Este script de Python permite generar las firmas para el correo siguiendo un archivo de configuración correspondiente a la entidad para la que es la firma (que incluye cosas como fuentes y colores) y otro archivo con los datos de las personas para las que generar la firma.

Aquí también se guardarán todas las firmas HTML que vaya haciendo para los correos electrónicos, principalmente para:

- [Delegación de Estudiantes de la Facultad de Ciencias (DEFC)](https://defc.ugr.es)
- [Delegación General de Estudiantes (DGE)](https://dge.ugr.es)
- [Asociación de Estudiantes de Matemáticas y Estadística de la UGR (AMAT)](https://amatugr.es)
- [Coordinadora de Representantes de Estudiantes de Universidades Públicas (CREUP)](https://www.creup.es)
- [XXVI Encuentro Nacional de Estudiantes de Matemáticas (ENEM)](https://enem.anem.es/2025) _(edición de 2025, histórica)_

Las firmas partieron de una base que supongo que será de @jesusjmma y, actualmente, utilizan iconos de [Tabler Icons](https://tabler-icons.io)

---

## Características

- ✅ Generación de firmas HTML a partir de plantillas Jinja2
- ✅ Soporte para múltiples configuraciones de organizaciones
- ✅ Validación de datos CSV y configuración JSON
- ✅ CLI con argumentos para automatización
- ✅ Previsualización de firmas generadas
- ✅ Compatibilidad mejorada con clientes de correo (uso de tablas HTML)
- ✅ Macros reutilizables para componentes comunes
- ✅ Accesibilidad mejorada (ARIA, textos alternativos, semántica)
- ✅ Escapado automático de datos de usuario (autoescape de Jinja2)

---

## Ejemplos de firmas

A continuación hay unas capturas de cómo se deberían de ver las firmas.

### Ejemplo de firma de la DEFC

Cuando los iconos cargan, la firma se debería de ver así:

![Firma de Iván Salido Cobo como Asesor de la DEFC en la que los iconos cargan](img/defc.png)

Y cuando no cargan, así:

![Firma de Iván Salido Cobo como Asesor de la DEFC en la que los iconos no cargan](img/defc-no-icons.png)

### Ejemplo de firma de la DGE

Cuando los iconos cargan, la firma se debería de ver así:

![Firma de Iván Salido Cobo como Vicecoordinador Académico de la DGE en la que los iconos cargan](img/dge.png)

Y cuando no cargan, así:

![Firma de Iván Salido Cobo como Vicecoordinador Académico de la DGE en la que los iconos no cargan](img/dge-no-icons.png)

### Ejemplo de firma de AMAT

Cuando los iconos cargan, la firma se debería de ver así:

![Firma de Iván Salido Cobo como Secretario de AMAT en la que los iconos cargan](img/amat.png)

Y cuando no cargan, así:

![Firma de Iván Salido Cobo como Secretario de AMAT en la que los iconos no cargan](img/amat-no-icons.png)

### Ejemplo de firma de CREUP

Cuando los iconos cargan, la firma se debería de ver así:

![Firma de Iván Salido Cobo como Vocal de Digitalización y Transparencia de CREUP en la que los iconos cargan](img/creup.png)

Y cuando no cargan, así:

![Firma de Iván Salido Cobo como Vocal de Digitalización y Transparencia de CREUP en la que los iconos no cargan](img/creup-no-icons.png)

### Ejemplo de firma del ENEM

Cuando los iconos cargan, la firma se debería de ver así:

![Firma de Iván Salido Cobo como Secretario y Tesorero del XXVI ENEM en la que los iconos cargan](img/enem.png)

Y cuando no cargan, así:

![Firma de Iván Salido Cobo como Secretario y Tesorero del XXVI ENEM en la que los iconos no cargan](img/enem-no-icons.png)

## Cómo usar las firmas

### En Thunderbird

Simplemente hay que irse a la configuración de la cuenta, marcar la casilla de utilizar un archivo como firma y seleccionar el archivo de firma descargado:

![Captura de pantalla de la ventana de configuración de la cuenta de Thunderbird](img/thunderbird.png)

### En Gmail

Primero hay que abrir en el navegador el archivo HTML de la firma, seleccionarlo todo con <kbd>Ctrl</kbd> + <kbd>A</kbd> y copiarlo con <kbd>Ctrl</kbd> + <kbd>C</kbd>.

En otra ventana con Gmail, hay que irse a los ajustes, ver todos los ajustes y, en la pestaña «General», al apartado de «Firma». Se crea una firma nueva y, en el campo de texto, se pega la firma con <kbd>Ctrl</kbd> + <kbd>V</kbd>.

No olvidar tampoco cambiar los «Valores predeterminados de firma» a la firma recién creada para que aparezca y guardar los cambios con el botón del final de la página.

![Captura de pantalla de la firma y los ajustes de Gmail](img/gmail.png)

### En Outlook

El procedimiento es igual que en Gmail. Primero hay que abrir en el navegador el archivo HTML de la firma, seleccionarlo todo con <kbd>Ctrl</kbd> + <kbd>A</kbd> y copiarlo con <kbd>Ctrl</kbd> + <kbd>C</kbd>.

Luego, en Outlook, hay que ir a los ajustes, al apartado «Cuenta» → «Firmas», crear una firma nueva y pegarla en el editor con <kbd>Ctrl</kbd> + <kbd>V</kbd>.

![Captura de pantalla de la firma y los ajustes de Outlook](img/outlook.png)

### En Webmail

El archivo de firma es un HTML y tiene la siguiente estructura:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title></title>
  </head>
  <body>
    <div>...</div>
  </body>
</html>
```

Pues para webmail recomiendo solo copiar la parte de

```html
<div>...</div>
```

Y pegarla en el apartado de configuración de Webmail, en «Identidades», dándole al botón que hay más a la derecha que parece `< >`. Este botón es para editar la firma como HTML. Se abrirá una ventana donde hay que pegar el código copiado, sustituyendo todo lo que hubiera antes.

![Captura de pantalla de la ventana de configuración de la cuenta de Webmail](img/webmail.png)

**¿Por qué la recomendación de copiar solo esa parte de la firma HTML?**

Simplemente porque pegando todo el contenido del archivo se pone un espacio en blanco al principio de la firma y es molesto eliminarlo manualmente.

## Cómo usar el script

Para generar firmas, primero hay que clonar o descargar este repositorio y tener instalado [uv](https://github.com/astral-sh/uv).

### Uso básico

```bash
# Modo interactivo (por defecto)
uv run main.py

# Especificar archivo de configuración
uv run main.py -c signatures.json

# Seleccionar perfil por ID (sin interacción)
uv run main.py -p ENEM

# Especificar archivo CSV de firmas
uv run main.py -l mis_firmas.csv

# Generar índice de previsualización
uv run main.py --preview

# Modo verbose (más información)
uv run main.py -v

# Modo silencioso (solo errores)
uv run main.py -q

# Combinar opciones
uv run main.py -c config.json -p CREUP -l firmas.csv --preview
```

### Opciones de línea de comandos

| Opción            | Descripción                                                        |
| ----------------- | ------------------------------------------------------------------ |
| `-c`, `--config`  | Archivo JSON de configuración (por defecto: `signatures.json`)     |
| `-p`, `--profile` | Seleccionar automáticamente el perfil con el ID especificado       |
| `-l`, `--list`    | Archivo CSV con la lista de firmas                                 |
| `--preview`       | Generar un `index.html` con todas las firmas para previsualización |
| `-v`, `--verbose` | Mostrar información detallada                                      |
| `-q`, `--quiet`   | Modo silencioso (solo errores)                                     |

### Configuración (`signatures.json`)

Lo primero que debes hacer es asegurarte de que tienes definida la configuración del tipo de firma en el archivo `signatures.json`. El archivo debe de seguir la siguiente estructura:

```json
[
  {
    "id": "EJEMPLO",
    "template": "original",
    "output_path": "EJEMPLO",
    "main_font": "Montserrat",
    "name_font": "Open Sans",
    "name_image": {
      "image": "https://example.com/logo.png",
      "description": "Logo de Mi Organización"
    },
    "color": "#3EB1C8",
    "organization": "Mi Organización",
    "organization_extra": "Entidad Superior (opcional)",
    "phone": "123 456 789",
    "phone_country_code": "+34",
    "internal_phone": "12345",
    "opt_mail": "info@ejemplo.es",
    "max_width": 315,
    "links": [
      {
        "url": "https://ejemplo.es",
        "image": "https://example.com/web-icon.png",
        "alt": "🌐",
        "description": "Sitio web de ejemplo"
      }
    ],
    "sponsor_text": "Con la colaboración de:",
    "sponsors": [
      {
        "url": "https://sponsor.com",
        "image": "https://sponsor.com/logo.png",
        "alt": "Sponsor",
        "description": "Patrocinador principal",
        "width": 100,
        "height": 50
      }
    ],
    "supporter_text": "Con el apoyo de:",
    "supporters": [
      {
        "url": "https://supporter.com",
        "image": "https://supporter.com/logo.png",
        "alt": "Supporter",
        "description": "Colaborador",
        "height": 55
      }
    ],
    "footer_address": "Calle Ejemplo, 123, 12345 Ciudad",
    "footer_text": "Texto legal opcional..."
  }
]
```

### Campos de configuración

| Campo                | Obligatorio | Descripción                                                                                                                                               |
| -------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                 | ✅           | Identificador de la configuración                                                                                                                         |
| `template`           | ✅           | Plantilla a usar: `original`, `wide-logo` o `upv`                                                                                                         |
| `output_path`        | ❌           | Carpeta de salida (por defecto usa `id`)                                                                                                                  |
| `main_font`          | ✅           | Fuente principal del texto. Puede ser una sola familia o una cadena con respaldos (ej: `Helvetica Neue, Helvetica, Arial`)                                |
| `name_font`          | ❌           | Fuente del nombre de la persona. Si falta, se usa `main_font`. Admite también una cadena con respaldos                                                    |
| `name_image`         | ❌           | Objeto `{image, url?, alt?, description?}` (ver abajo). En `original`/`wide-logo` es el logo de la organización; en `upv` es la foto personal por defecto |
| `color`              | ✅           | Color hexadecimal (ej: `#3EB1C8`)                                                                                                                         |
| `organization`       | ✅           | Nombre de la organización                                                                                                                                 |
| `organization_extra` | ❌           | Organización superior/adicional                                                                                                                           |
| `phone`              | ❌           | Número de teléfono (sin código de país)                                                                                                                   |
| `phone_country_code` | ❌           | Código de país (ej: `+34`)                                                                                                                                |
| `internal_phone`     | ❌           | Extensión interna                                                                                                                                         |
| `opt_mail`           | ❌           | Email alternativo (se muestra si no hay teléfono)                                                                                                         |
| `max_width`          | ❌           | Ancho máximo de la firma en píxeles (máximo `440`)                                                                                                        |
| `links`              | ❌           | Lista de enlaces sociales                                                                                                                                 |
| `sponsor_text`       | ❌           | Texto sobre los patrocinadores                                                                                                                            |
| `sponsors`           | ❌           | Lista de patrocinadores                                                                                                                                   |
| `supporter_text`     | ❌           | Texto sobre los colaboradores                                                                                                                             |
| `supporters`         | ❌           | Lista de colaboradores                                                                                                                                    |
| `footer_address`     | ❌           | Dirección postal                                                                                                                                          |
| `footer_text`        | ❌           | Texto legal del footer (admite HTML, ver nota)                                                                                                            |

Campos específicos de la plantilla `upv` (todos opcionales):

| Campo                     | Descripción                                                                                                                                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `photo`                   | URL de la foto personal (círculo izquierdo). Suele indicarse por persona en el CSV; si falta, se usa `name_image`                                                                                                                     |
| `organization_logo`       | Objeto logo `{image, url?, alt?, width?, height?}` de la organización (arriba a la derecha, alineado a la izquierda, sobre las redes). Se limita a **140px de ancho y 50px de alto** como máximo (se reescala manteniendo proporción) |
| `organization_extra_logo` | Objeto logo `{image, url?, alt?, width?, height?}` de la organización superior (abajo a la derecha, ej: el logo de la UPV). Su `width` (140 por defecto) define el ancho sobre el que se reparten las redes                           |
| `contact_height`          | Altura en píxeles de la columna de logos (por defecto `122`). El bloque de contacto reparte su espaciado para llenar esa altura y alinear la última línea con el pie del logo; ajústala si cambias el tamaño de los logos             |
| `website_url`             | URL de la página web que se muestra en el bloque de contacto                                                                                                                                                                          |
| `website_text`            | Texto visible del enlace web (por defecto se muestra la propia URL)                                                                                                                                                                   |
| `location`                | Texto de ubicación (ej: `Edificio 4K`)                                                                                                                                                                                                |
| `location_url`            | URL del enlace de la ubicación (ej: plano del campus)                                                                                                                                                                                 |
| `location_icon`           | URL del icono que precede a la ubicación (ej: un marcador de mapa)                                                                                                                                                                    |

En la cabecera de `upv`, bajo el nombre van dos líneas en negrita: `position` (cargo) y `organization` (unidad); `position` se muestra tal cual, sin partirse. La línea inferior del bloque de contacto muestra `organization_extra` (o `organization` si no está).

Distribución de imágenes en `upv`: a la **izquierda** la foto personal (`photo`/`name_image`, círculo); a la **derecha**, de arriba a abajo, el logo de la organización (`organization_logo`), las redes sociales (`links`) y el logo de la organización superior (`organization_extra_logo`).

**Iconos de redes en `upv`:** se muestran planos (no como avatar redondo), con **alto fijo** y ancho automático, sobre el ancho del logo de la organización superior (`organization_extra_logo.width`, 140 por defecto):

- Si hay `organization_logo`: alto **13px**, hasta **5 por línea**.
- Si no: alto **15px**, hasta **4 por línea**.
- Una línea de 4 o más iconos se reparte a lo largo del ancho; una de 3 o menos se alinea a la izquierda. La separación mínima entre iconos es de **10px**. Los iconos que sobren pasan a una nueva línea con las mismas reglas.

> **Nota:** si no hay foto (`photo` ni `name_image`), la firma se renderiza sin ese hueco (el contacto queda alineado a la izquierda).

> **Nota sobre HTML y escapado:** los valores se escapan automáticamente (autoescape de Jinja2) para evitar romper el HTML o inyectar marcado con caracteres como `&`, `<` o `>`. La única excepción es `footer_text`, que se renderiza como HTML sin escapar para permitir enlaces (`<a>`) y saltos de línea (`<br>`) en los textos legales.

> **Nota sobre imágenes:** los campos de imagen (`image`, `photo`, `location_icon`) aceptan una URL `http(s)` o una **ruta local relativa al HTML generado** (ej: `img/CEUPV.png`, sirviendo las imágenes desde `{output_path}/img/`). Otros esquemas (`data:`, `file:`, `javascript:`, …) se rechazan. Los campos de enlace (`url`, `website_url`, `location_url`) deben ser siempre URLs `http(s)`.

#### Formato de `name_image`

Debe ser un objeto con las propiedades de la imagen:

```json
"name_image": {
  "image": "https://example.com/logo.png",
  "url": "https://example.com",
  "alt": "Logo",
  "description": "Ir al sitio web"
}
```

| Campo         | Obligatorio | Descripción                                    |
| ------------- | ----------- | ---------------------------------------------- |
| `image`       | ✅           | URL http(s) o ruta local de la imagen          |
| `url`         | ❌           | URL del enlace (si hay, la imagen es clicable) |
| `alt`         | ❌           | Texto alternativo (por defecto: 👤)             |
| `description` | ❌           | Descripción (se usa en title y aria-label)     |

#### Formato de `links`

| Campo         | Obligatorio | Descripción                                |
| ------------- | ----------- | ------------------------------------------ |
| `url`         | ✅           | URL del enlace                             |
| `image`       | ✅           | URL http(s) o ruta local del icono         |
| `alt`         | ❌           | Texto alternativo (emoji recomendado)      |
| `description` | ❌           | Descripción (se usa en title y aria-label) |

#### Formato de `sponsors` y `supporters`

| Campo         | Obligatorio | Descripción                                |
| ------------- | ----------- | ------------------------------------------ |
| `url`         | ❌           | URL del enlace (si no hay, no es clicable) |
| `image`       | ✅           | URL http(s) o ruta local del logo          |
| `alt`         | ❌           | Texto alternativo                          |
| `description` | ❌           | Descripción (se usa en title y aria-label) |
| `width`       | ❌           | Ancho en píxeles                           |
| `height`      | ❌           | Alto en píxeles                            |

### Plantillas disponibles

| Plantilla   | Descripción                                                                                                                                                                                                                                  |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `original`  | Diseño clásico con imagen circular y barra horizontal                                                                                                                                                                                        |
| `wide-logo` | Logo ancho arriba con barra vertical al lado del contenido                                                                                                                                                                                   |
| `upv`       | Estilo institucional UPV: nombre y cargo arriba con barra horizontal; foto personal opcional a la izquierda; contacto en el centro; a la derecha, logo de la organización sobre las redes sociales sobre el logo de la organización superior |

#### Campos que renderiza cada plantilla

La **obligatoriedad de los campos es la misma para todas las plantillas** (se define en el esquema, no por plantilla): solo `id`, `template`, `main_font`, `color` y `organization` son obligatorios; el resto son opcionales. Lo que cambia es **qué campos dibuja** cada plantilla según su diseño:

| Campo                                                                                                                                  |       `original`        |       `wide-logo`       |       `upv`       |
| -------------------------------------------------------------------------------------------------------------------------------------- | :---------------------: | :---------------------: | :---------------: |
| `name`, `position`, `organization`, `color`, fuentes, `max_width`                                                                      |            ✅            |            ✅            |         ✅         |
| `phone` / `internal_phone`, `mail`, `links`                                                                                            |            ✅            |            ✅            |         ✅         |
| `sponsors` / `supporters`, `footer_address` / `footer_text`                                                                            |            ✅            |            ✅            |         ✅         |
| `organization_extra`                                                                                                                   |            ✅            |            ✅            |         ✅         |
| `opt_mail`                                                                                                                             |            ✅            |            ✅            |         ✅         |
| `name_image`                                                                                                                           | logo de la organización | logo de la organización | **foto personal** |
| `photo`, `organization_logo`, `organization_extra_logo`, `website_url` / `website_text`, `location` / `location_url` / `location_icon` |            ❌            |            ❌            |         ✅         |

> **`name_image`** cambia de significado según la plantilla: en `original`/`wide-logo` es el logo de la organización; en `upv` es la foto personal por defecto (que la columna `photo` del CSV puede sobrescribir por persona).
>
> Los campos de la última fila son propios del diseño institucional de `upv`; si se definen en una configuración con plantilla `original`/`wide-logo` se ignoran (no rompen nada).

### Lista de firmas (CSV)

Una vez esté la configuración definida hay que crear la lista de firmas a generar, que es un archivo CSV (por defecto `{id en minúsculas}_list.csv`, ej: `enem_list.csv`).

> **Plantilla:** el archivo [`signatures_list.csv`](signatures_list.csv) contiene solo la fila de cabeceras y sirve como plantilla de partida para crear nuevas listas: cópialo, renómbralo a `{id}_list.csv` y rellena las filas.

#### Columnas obligatorias

```csv
name,position,mail
```

#### Columnas opcionales

Estas columnas, si tienen valor, sobrescriben la configuración general:

```csv
output,phone,phone_country_code,internal_phone,opt_mail,organization_extra,main_font,name_font,max_width,name_image,color,organization,photo,website_url,website_text,location,location_url,location_icon
```

> **Nota:** las columnas `photo`, `website_url`, `website_text`, `location`, `location_url` y `location_icon` solo las usa la plantilla `upv`. `photo` (la foto personal) suele indicarse por persona en el CSV. Los logos `organization_logo`/`organization_extra_logo` son objetos y solo se definen en `signatures.json`.

> **Nota:** Usa `None` en una celda para eliminar un valor opcional de la configuración general para esa firma específica.
>
> **Nota:** la columna `name_image` se acepta en la cabecera por compatibilidad, pero **se ignora**: al ser un objeto (no un texto) no puede construirse desde una celda CSV. Defínela solo en `signatures.json`.

#### Ejemplo de CSV

```csv
Name,Position,Mail,Output,Phone,internal_phone
Ana García,Presidenta,presidencia@ejemplo.es,Firma Presidenta,123 456 789,12345
Juan López,Secretario,secretaria@ejemplo.es,Firma Secretario,,None
```

## Accesibilidad

Las firmas incluyen varias características para mejorar la accesibilidad:

| Característica         | Descripción                                                                                                 |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- |
| `role="presentation"`  | Las tablas usadas para maquetación se marcan como decorativas para que los lectores de pantalla las ignoren |
| `aria-hidden="true"`   | Los elementos decorativos (barras de color, iconos dentro de enlaces) se ocultan a lectores de pantalla     |
| `aria-label`           | Los enlaces con iconos usan `description` como etiqueta accesible descriptiva                               |
| `alt` en imágenes      | Todas las imágenes tienen texto alternativo (emoji por defecto: 👤, 🌐, etc.)                                 |
| `title` en enlaces     | Los enlaces muestran tooltip con la descripción al pasar el ratón                                           |
| `role="img"` en avatar | La imagen del avatar/logo se marca explícitamente como imagen semántica                                     |

> **Tip:** Para una accesibilidad óptima, configura `alt` (emoji o texto corto) y `description` (texto descriptivo completo) en los enlaces e imágenes.

## Clientes de correo soportados

Las firmas ahora usan tablas HTML en lugar de flexbox para mejorar la compatibilidad con clientes de correo. Las pruebas no han sido muy exhaustivas, pero la firma en algunos sitios va bien :green_circle:, regulinchi _(se ve bien en general pero puede fallar en algún detalle)_ :yellow_circle: y mal :red_circle:. Esta es la lista:

:green_circle: Webmail

:green_circle: Thunderbird

:green_circle: Outlook web

:green_circle: Outlook móvil

:green_circle: Gmail web

:green_circle: Gmail móvil

:yellow_circle: Thunderbird móvil

:red_circle: Canary Mail

## Estructura del proyecto

```
mail-signatures/
├── main.py              # Script principal
├── schemas.py           # Validación de datos
├── signatures.json      # Configuración de organizaciones
├── *_list.csv           # Listas de firmas por organización
├── templates/
│   ├── _base.html.j2    # Plantilla base con estructura común
│   ├── _macros.html.j2  # Macros reutilizables
│   ├── original.html.j2 # Plantilla clásica
│   ├── wide-logo.html.j2# Plantilla con logo ancho
│   └── upv.html.j2      # Plantilla institucional UPV
└── {OUTPUT}/            # Firmas generadas por organización
```

## Desarrollo

### Crear una nueva plantilla

1. Crea un archivo `templates/mi-plantilla.html.j2`
2. Extiende la plantilla base: `{% extends "templates/_base.html.j2" %}`
3. Sobrescribe los bloques necesarios (`header`, `content`, `links`, `sponsors`, etc.)
4. Añade el nombre `mi-plantilla` en el campo `template` de la configuración

> **Nota:** También puedes crear una plantilla desde cero importando los macros directamente con `{% from "templates/_macros.html.j2" import ... %}`, pero extender `_base.html.j2` es más sencillo.

### Macros disponibles

| Macro                                                                     | Descripción                           |
| ------------------------------------------------------------------------- | ------------------------------------- |
| `social_link(link, size)`                                                 | Renderiza un enlace social individual |
| `social_links_bar(links, size, max_width)`                                | Barra de enlaces sociales             |
| `sponsor_image(item, max_width)`                                          | Imagen de sponsor/supporter           |
| `sponsors_section(text, items, color, max_width, with_bar)`               | Sección completa de sponsors          |
| `footer(footer_address, footer_text, color, max_width)`                   | Footer con dirección y texto legal    |
| `contact_info(phone, phone_country_code, internal_phone, mail, opt_mail)` | Información de contacto               |
| `name_image_block(name_image, organization, size, rounded, wide)`         | Bloque de imagen/avatar con nombre    |
