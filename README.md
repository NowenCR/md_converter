# ⬡ MD Forge — Convertidor de Archivos a Markdown

Aplicación de escritorio con interfaz gráfica para convertir archivos de múltiples formatos a Markdown (`.md`), desarrollada en Python con `tkinter`.
Cualquier .exe fue generado con auto-py-to-exe
pip install auto-py-to-exe

---

## 🖥️ Capturas

Interfaz oscura y minimalista con soporte de múltiples archivos en cola, vista previa, y barra de progreso en tiempo real.

---

## 📦 Formatos Soportados

| Formato       | Extensión(es)       | Librería requerida   |
|---------------|---------------------|----------------------|
| PDF           | `.pdf`              | `pdfplumber` / `PyPDF2` |
| Word          | `.docx`             | `python-docx`        |
| Word (legacy) | `.doc`              | `antiword` (sistema) |
| Texto plano   | `.txt`              | *(ninguna)*          |
| RTF           | `.rtf`              | `striprtf`           |
| HTML          | `.html`, `.htm`     | `beautifulsoup4`     |
| CSV           | `.csv`              | *(ninguna)*          |
| ODT           | `.odt`              | `odfpy`              |
| EPUB          | `.epub`             | `ebooklib`           |
| Markdown      | `.md` (passthrough) | *(ninguna)*          |

---

## ⚙️ Instalación

### 1. Requisitos previos

- Python **3.8** o superior
- `pip`

### 2. Clonar / descargar el proyecto

```bash
git clone <repo_url>
cd md_converter
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> En Linux con Python del sistema, puede necesitar:
> ```bash
> pip install -r requirements.txt --break-system-packages
> ```

### 4. Ejecutar la aplicación

```bash
python app.py
```

---

## 🚀 Uso

1. **Agregar archivos** — Haz clic en `＋ Add Files` para seleccionar uno o varios archivos.
2. **Directorio de salida** — Selecciona dónde se guardarán los archivos `.md`.
3. **Convertir** — Clic en `▶ CONVERT TO MARKDOWN`. Cada archivo mostrará su estado en tiempo real.
4. **Preview** — Selecciona un archivo y haz clic en `Preview` para ver el Markdown generado antes o después de convertir.
5. **Abrir carpeta** — Haz clic en `Open Output Folder` para abrir el directorio de salida.

---

## 🗂️ Estructura del Proyecto

```
md_converter/
├── app.py              # Punto de entrada y lógica principal
├── converter.py        # Motor de conversión por formato
├── ui_components.py    # Interfaz gráfica (tkinter)
├── requirements.txt    # Dependencias Python
└── README.md           # Este archivo
```

---

## 🛠️ Detalles Técnicos

- **PDF**: Extrae texto y tablas con `pdfplumber`; detecta automáticamente páginas y encabezados.
- **DOCX**: Respeta estilos de Word (Heading 1-4, listas, texto en negrita/cursiva).
- **HTML**: Convierte la estructura semántica (h1-h6, p, ul, table, blockquote, pre, a, img).
- **CSV**: Genera tablas Markdown con encabezados y separadores automáticos.
- **Texto plano**: Detecta líneas en MAYÚSCULAS como posibles encabezados.
- **Conversión multihilo**: Los archivos se convierten en un hilo separado para no bloquear la UI.

---

## 🐛 Solución de Problemas

| Problema | Solución |
|---|---|
| `No module named 'pdfplumber'` | `pip install pdfplumber` |
| `No module named 'docx'` | `pip install python-docx` |
| No puede convertir `.doc` | Instalar `antiword`: `sudo apt install antiword` |
| Tkinter no disponible | `sudo apt install python3-tk` (Linux) |

---

## 📄 Licencia

MIT — libre para uso personal y comercial.
