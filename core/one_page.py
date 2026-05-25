from playwright.sync_api import sync_playwright

TUNING_STEPS = [
    ("--page-margin", 20, 12, -2, "mm"),
    ("--section-spacing", 12, 4, -2, "pt"),
    ("--entry-spacing", 8, 2, -2, "pt"),
    ("--line-height", 1.5, 1.2, -0.05, ""),
    ("--body-font-size", 10.5, 8.5, -0.5, "pt"),
    ("--h2-font-size", 14, 11, -0.5, "pt"),
]


def _get_page_count_playwright(html: str) -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        pdf_bytes = page.pdf(format="A4", print_background=True)
        browser.close()
    import fitz
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    count = len(doc)
    doc.close()
    return count


def _build_override_css(overrides: dict) -> str:
    if not overrides:
        return ""
    props = "\n".join(f"    {k}: {v};" for k, v in overrides.items())
    lines = [
        "<style>",
        ":root {",
        props,
        "}",
        "</style>",
    ]
    return "\n".join(lines)


def _inject_overrides(html: str, overrides: dict) -> str:
    css_block = _build_override_css(overrides)
    if not css_block:
        return html
    return html.replace("</head>", css_block + "\n</head>")


def fit_to_one_page(html_content: str, max_iterations: int = 30) -> tuple:
    if _get_page_count_playwright(html_content) <= 1:
        from .renderer import render_pdf_playwright
        pdf_bytes = render_pdf_playwright(html_content)
        return html_content, pdf_bytes

    overrides = {}
    current_html = html_content
    iterations = 0

    for var_name, initial, minimum, step, unit in TUNING_STEPS:
        if _get_page_count_playwright(current_html) <= 1:
            break

        value = initial
        while value + step >= minimum and iterations < max_iterations:
            value += step
            value = round(value, 2)
            overrides[var_name] = f"{value}{unit}" if unit else str(value)
            current_html = _inject_overrides(html_content, overrides)
            iterations += 1
            if _get_page_count_playwright(current_html) <= 1:
                break

    from .renderer import render_pdf_playwright
    pdf_bytes = render_pdf_playwright(current_html)
    return current_html, pdf_bytes
