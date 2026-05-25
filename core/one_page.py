TUNING_STEPS = [
    ("--page-margin", 20, 12, -2, "mm"),
    ("--section-spacing", 12, 4, -2, "pt"),
    ("--entry-spacing", 8, 2, -2, "pt"),
    ("--line-height", 1.5, 1.2, -0.05, ""),
    ("--body-font-size", 10.5, 8.5, -0.5, "pt"),
    ("--h2-font-size", 14, 11, -0.5, "pt"),
]


def _get_page_count(html: str) -> int:
    import weasyprint
    doc = weasyprint.HTML(string=html)
    return len(doc.render().pages)


def _build_override_css(overrides: dict) -> str:
    if not overrides:
        return ""
    props = "\n".join(f"    {k}: {v};" for k, v in overrides.items())
    lines = [
        "<style>",
        ":root {",
        props,
        "}",
        "@page {",
        f"    margin: {overrides.get('--page-margin', '20mm')};",
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
    import weasyprint
    if _get_page_count(html_content) <= 1:
        pdf_bytes = weasyprint.HTML(string=html_content).write_pdf()
        return html_content, pdf_bytes

    overrides = {}
    current_html = html_content
    iterations = 0

    for var_name, initial, minimum, step, unit in TUNING_STEPS:
        if _get_page_count(current_html) <= 1:
            break

        value = initial
        while value + step >= minimum and iterations < max_iterations:
            value += step
            value = round(value, 2)
            overrides[var_name] = f"{value}{unit}" if unit else str(value)
            current_html = _inject_overrides(html_content, overrides)
            iterations += 1
            if _get_page_count(current_html) <= 1:
                break

    pdf_bytes = weasyprint.HTML(string=current_html).write_pdf()
    return current_html, pdf_bytes
