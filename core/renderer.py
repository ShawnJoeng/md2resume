from __future__ import annotations

import base64
import re
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Optional

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


def render_pdf(html_content: str) -> bytes:
    import weasyprint
    doc = weasyprint.HTML(string=html_content, base_url=str(TEMPLATES_DIR))
    return doc.write_pdf()


def render_png(pdf_bytes: bytes, dpi: int = 200) -> bytes:
    try:
        from pdf2image import convert_from_bytes
        images = convert_from_bytes(pdf_bytes, dpi=dpi, first_page=1, last_page=1)
        buf = BytesIO()
        images[0].save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        import weasyprint
        doc = weasyprint.HTML(string="<html><body></body></html>")
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
        pdf_bytes = render_pdf(html_content)

    png_bytes = render_png(pdf_bytes)

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
