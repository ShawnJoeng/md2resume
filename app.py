import os

import gradio_client.utils as _gc_utils
_orig_get_type = _gc_utils.get_type
_gc_utils.get_type = lambda schema: "Any" if not isinstance(schema, dict) else _orig_get_type(schema)
_orig_schema_fn = _gc_utils._json_schema_to_python_type
_gc_utils._json_schema_to_python_type = lambda schema, defs: "Any" if not isinstance(schema, dict) else _orig_schema_fn(schema, defs)

import gradio as gr
from pathlib import Path

from core.parser import parse_markdown
from core.renderer import generate_all
from core.llm import convert_to_resume

EXAMPLES_DIR = Path(__file__).parent / "examples"

DEFAULT_API_KEY = os.environ.get("LIBINFER_SK", "")
_raw_url = os.environ.get("LIBINFER_URL", "https://api.openai.com")
DEFAULT_BASE_URL = _raw_url.rstrip("/") + "/v1" if not _raw_url.rstrip("/").endswith("/v1") else _raw_url
DEFAULT_MODEL = os.environ.get("LIBINFER_MODEL", "claude-sonnet-4-6")


def _read_md_file(file) -> str:
    if file is None:
        return ""
    if hasattr(file, "read"):
        return file.read().decode("utf-8")
    return Path(file).read_text(encoding="utf-8")


def smart_convert(raw_text, raw_file, api_key, base_url, model):
    content = raw_text.strip() if raw_text and raw_text.strip() else ""
    if not content and raw_file is not None:
        content = _read_md_file(raw_file)

    if not content:
        raise gr.Error("请粘贴或上传你的原始内容")
    if not api_key:
        raise gr.Error("请输入 API Key")

    try:
        result = convert_to_resume(
            raw_content=content,
            api_key=api_key,
            base_url=base_url or "https://api.openai.com/v1",
            model=model or "claude-sonnet-4-6",
        )
        return result
    except Exception as e:
        raise gr.Error(f"智能转换失败: {str(e)}")


def generate_resume(md_text, photo, fit_one_page):
    md_content = md_text.strip() if md_text and md_text.strip() else ""

    if not md_content:
        raise gr.Error("请先粘贴或生成简历 Markdown 内容")

    resume_data = parse_markdown(md_content)

    photo_path = None
    if photo is not None:
        photo_path = photo

    outputs = generate_all(
        resume_data=resume_data,
        template_name="professional",
        photo_path=photo_path,
        fit_one_page=fit_one_page,
    )

    return outputs["pdf"], outputs["html"], outputs["png"], outputs["png"]


with gr.Blocks(
    title="md2resume - Markdown 转精美简历",
    theme=gr.themes.Soft(),
    css=".gradio-container { max-width: 800px !important; }",
) as app:
    gr.Markdown(
        """
# md2resume

**Markdown + 证件照 → 精美简历**（PDF / HTML / PNG）

粘贴任意格式的经历内容，AI 自动整理为 STAR 法则格式的专业简历
"""
    )

    gr.Markdown("### AI 配置")
    api_key = gr.Textbox(
        label="API Key",
        type="password",
        value=DEFAULT_API_KEY,
        placeholder="sk-...",
        lines=1,
        max_lines=1,
    )
    base_url = gr.Textbox(
        label="Base URL",
        value=DEFAULT_BASE_URL,
        placeholder="https://api.openai.com/v1",
        lines=1,
        max_lines=1,
    )
    model = gr.Textbox(
        label="模型",
        value=DEFAULT_MODEL,
        placeholder="claude-sonnet-4-6",
        lines=1,
        max_lines=1,
    )

    gr.Markdown("### 输入内容")
    raw_file = gr.File(
        label="上传文件（可选）",
        file_types=[".md", ".markdown", ".txt"],
    )
    raw_text = gr.Textbox(
        label="粘贴原始内容（任意格式：旧简历、笔记、工作总结等）",
        lines=10,
        placeholder="例如：\n我叫张三，2020年从北大计算机硕士毕业，现在在字节跳动做后端开发...\n\n或者直接粘贴已格式化的 Markdown 简历内容",
    )
    convert_btn = gr.Button("智能转换（AI 整理为标准格式）", variant="secondary")

    gr.Markdown("### 简历 Markdown（可编辑）")
    md_text = gr.Textbox(
        label="标准 Markdown 内容",
        lines=12,
        placeholder="# 姓名\n\n- 手机: 138-0000-0000\n- 邮箱: example@email.com\n\n## 教育经历\n...",
        interactive=True,
    )

    photo = gr.Image(
        label="证件照（可选）",
        type="filepath",
        sources=["upload"],
        height=150,
    )
    fit_one_page = gr.Checkbox(
        label="自动适配一页",
        value=True,
    )

    generate_btn = gr.Button("生成简历", variant="primary", size="lg")

    gr.Markdown("### 生成结果")
    preview_img = gr.Image(label="预览", type="filepath")
    with gr.Row():
        pdf_output = gr.File(label="下载 PDF")
        html_output = gr.File(label="下载 HTML")
        png_output = gr.File(label="下载 PNG")

    convert_btn.click(
        fn=smart_convert,
        inputs=[raw_text, raw_file, api_key, base_url, model],
        outputs=[md_text],
    )

    generate_btn.click(
        fn=generate_resume,
        inputs=[md_text, photo, fit_one_page],
        outputs=[pdf_output, html_output, png_output, preview_img],
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    app.launch(server_name="0.0.0.0", server_port=port)
