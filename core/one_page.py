from playwright.sync_api import sync_playwright


def _render_and_count(html: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        pdf_bytes = page.pdf(
            format="A4",
            margin={"top": "10mm", "bottom": "10mm", "left": "12mm", "right": "12mm"},
            print_background=True,
        )
        browser.close()
    import fitz
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    count = len(doc)
    doc.close()
    return pdf_bytes, count


def _inject_scale_css(html: str, scale: float) -> str:
    css = f"""<style>
body {{
    font-size: {8.5 * scale}pt !important;
    line-height: {1.3 * scale + 0.2} !important;
}}
.section {{
    margin-bottom: {4 * scale}pt !important;
}}
.entry {{
    margin-bottom: {3 * scale}pt !important;
}}
.entry-details li {{
    margin-bottom: {0.5 * scale}pt !important;
    line-height: {1.4 * scale + 0.1} !important;
}}
h2 {{
    font-size: {10 * scale}pt !important;
    margin-bottom: {3 * scale}pt !important;
}}
.entry-title {{
    font-size: {9 * scale}pt !important;
}}
.resume-header {{
    margin-bottom: {6 * scale}pt !important;
}}
</style>"""
    return html.replace("</head>", css + "\n</head>")


def fit_to_one_page(html_content: str) -> tuple:
    pdf_bytes, count = _render_and_count(html_content)
    if count <= 1:
        return html_content, pdf_bytes

    scale = 1.0
    current_html = html_content
    while count > 1 and scale > 0.7:
        scale -= 0.05
        current_html = _inject_scale_css(html_content, scale)
        pdf_bytes, count = _render_and_count(current_html)

    return current_html, pdf_bytes
