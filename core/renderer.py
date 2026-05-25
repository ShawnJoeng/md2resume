from __future__ import annotations

import base64
import re
import tempfile
from io import BytesIO
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup
from PIL import Image

from .parser import ResumeData

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def _md_inline(text: str) -> Markup:
    """Convert Markdown inline formatting to HTML."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return Markup(text)


def _encode_photo(photo_path: str, max_size: tuple[int, int] = (300, 400)) -> str:
    img = Image.open(photo_path)
    img.thumbnail(max_size, Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def render_html(resume_data: ResumeData, template_name: str = "classic") -> str:
    template_dir = TEMPLATES_DIR / template_name
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    env.filters['md'] = _md_inline
    template = env.get_template("template.html")
    css_path = template_dir / "style.css"
    css_content = css_path.read_text(encoding="utf-8")
    return template.render(resume=resume_data, css=css_content)


def render_pdf_playwright(html_content: str) -> bytes:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        pdf_bytes = page.pdf(
            format="A4",
            margin={"top": "10mm", "bottom": "10mm", "left": "12mm", "right": "12mm"},
            print_background=True,
        )
        browser.close()
    return pdf_bytes


def render_png_from_pdf(pdf_bytes: bytes) -> bytes:
    try:
        import fitz
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        mat = fitz.Matrix(2.0, 2.0)
        pages = []
        total_height = 0
        width = 0
        for page in doc:
            pix = page.get_pixmap(matrix=mat)
            pages.append(pix)
            total_height += pix.height
            width = max(width, pix.width)
        combined = Image.new("RGB", (width, total_height), "white")
        y_offset = 0
        for pix in pages:
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            combined.paste(img, (0, y_offset))
            y_offset += pix.height
        buf = BytesIO()
        combined.save(buf, format="PNG")
        return buf.getvalue()
    except ImportError:
        img = Image.new("RGB", (1654, 2339), "white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()


def generate_all(
    resume_data: ResumeData,
    template_name: str = "classic",
    photo_path: str | None = None,
    fit_one_page: bool = False,
) -> dict[str, str]:
    if photo_path:
        resume_data.photo_base64 = _encode_photo(photo_path)

    html_content = render_html(resume_data, template_name)

    if fit_one_page:
        from .one_page import fit_to_one_page
        html_content, pdf_bytes = fit_to_one_page(html_content)
    else:
        pdf_bytes = render_pdf_playwright(html_content)

    png_bytes = render_png_from_pdf(pdf_bytes)

    output_dir = tempfile.mkdtemp(prefix="md2resume_")

    pdf_path = Path(output_dir) / "resume.pdf"
    pdf_path.write_bytes(pdf_bytes)

    html_path = Path(output_dir) / "resume.html"
    html_path.write_text(html_content, encoding="utf-8")

    png_path = Path(output_dir) / "resume.png"
    png_path.write_bytes(png_bytes)

    return {
        "pdf": str(pdf_path),
        "html": str(html_path),
        "png": str(png_path),
    }
