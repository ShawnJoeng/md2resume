import gradio as gr
from pathlib import Path

from core.parser import parse_markdown
from core.renderer import generate_all
from core.llm import refine_resume, convert_to_resume

EXAMPLES_DIR = Path(__file__).parent / "examples"


def _read_md_file(file) -> str:
    if file is None:
        return ""
    if hasattr(file, "read"):
        return file.read().decode("utf-8")
    return Path(file).read_text(encoding="utf-8")


def generate_resume(md_file, md_text, photo, template_name, fit_one_page):
    md_content = md_text.strip() if md_text and md_text.strip() else ""
    if not md_content and md_file is not None:
        md_content = _read_md_file(md_file)

    if not md_content:
        raise gr.Error("请上传 Markdown 文件或在文本框中粘贴简历内容")

    resume_data = parse_markdown(md_content)

    template_map = {"经典单栏": "classic", "现代双栏": "modern", "极简风格": "minimal"}
    tpl = template_map.get(template_name, "classic")

    photo_path = None
    if photo is not None:
        photo_path = photo

    outputs = generate_all(
        resume_data=resume_data,
        template_name=tpl,
        photo_path=photo_path,
        fit_one_page=fit_one_page,
    )

    return outputs["pdf"], outputs["html"], outputs["png"], outputs["png"]


def polish_with_llm(md_file, md_text, api_key, base_url, model):
    md_content = md_text.strip() if md_text and md_text.strip() else ""
    if not md_content and md_file is not None:
        md_content = _read_md_file(md_file)

    if not md_content:
        raise gr.Error("请上传 Markdown 文件或在文本框中粘贴简历内容")
    if not api_key:
        raise gr.Error("请输入 API Key")

    try:
        result = refine_resume(
            md_content=md_content,
            api_key=api_key,
            base_url=base_url or "https://api.openai.com/v1",
            model=model or "gpt-4o-mini",
        )
        return result
    except Exception as e:
        raise gr.Error(f"AI 润色失败: {str(e)}")


def load_example(lang):
    if lang == "中文示例":
        path = EXAMPLES_DIR / "sample_zh.md"
    else:
        path = EXAMPLES_DIR / "sample_en.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def convert_raw_content(raw_text, raw_file, api_key, base_url, model):
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
            model=model or "gpt-4o-mini",
        )
        return result
    except Exception as e:
        raise gr.Error(f"智能转换失败: {str(e)}")


with gr.Blocks(
    title="md2resume - Markdown 转精美简历",
    theme=gr.themes.Soft(),
    css=".gradio-container { max-width: 1200px !important; }",
) as app:
    gr.Markdown(
        """
# md2resume

**Markdown + 证件照 → 精美简历**（PDF / HTML / PNG）

支持多套模板、一页自适应、AI 智能润色、智能转换
"""
    )

    with gr.Tabs():
        with gr.Tab("生成简历"):
            with gr.Row():
                with gr.Column(scale=1):
                    md_file = gr.File(
                        label="上传 Markdown 文件",
                        file_types=[".md", ".markdown", ".txt"],
                    )
                    md_text = gr.Textbox(
                        label="或直接粘贴 Markdown 内容",
                        lines=12,
                        placeholder="# 张三\n\n- 手机: 138-0000-0000\n- 邮箱: example@email.com\n\n## 教育经历\n...",
                    )
                    photo = gr.Image(
                        label="证件照（可选）",
                        type="filepath",
                    )
                    template_name = gr.Dropdown(
                        label="选择模板",
                        choices=["经典单栏", "现代双栏", "极简风格"],
                        value="经典单栏",
                    )
                    fit_one_page = gr.Checkbox(
                        label="自动适配一页",
                        value=False,
                    )
                    generate_btn = gr.Button("生成简历", variant="primary", size="lg")

                with gr.Column(scale=1):
                    preview_img = gr.Image(label="预览", type="filepath")
                    with gr.Row():
                        pdf_output = gr.File(label="下载 PDF")
                        html_output = gr.File(label="下载 HTML")
                        png_output = gr.File(label="下载 PNG")

            generate_btn.click(
                fn=generate_resume,
                inputs=[md_file, md_text, photo, template_name, fit_one_page],
                outputs=[pdf_output, html_output, png_output, preview_img],
            )

        with gr.Tab("智能转换"):
            gr.Markdown(
                """
### 随便粘贴，AI 帮你整理成标准简历

不需要记格式！把你的经历、旧简历、笔记等任意内容粘贴进来，AI 会自动提取信息并生成标准 Markdown 简历格式。
"""
            )
            with gr.Row():
                with gr.Column():
                    convert_api_key = gr.Textbox(
                        label="API Key",
                        type="password",
                        placeholder="sk-...",
                    )
                    convert_base_url = gr.Textbox(
                        label="API Base URL",
                        value="https://api.openai.com/v1",
                        placeholder="https://api.openai.com/v1",
                    )
                    convert_model = gr.Textbox(
                        label="模型名称",
                        value="gpt-4o-mini",
                        placeholder="gpt-4o-mini",
                    )
                with gr.Column():
                    convert_file = gr.File(
                        label="或上传文件",
                        file_types=[".md", ".txt", ".doc"],
                    )

            convert_input = gr.Textbox(
                label="粘贴你的原始内容（随意格式均可）",
                lines=12,
                placeholder="例如：\n我叫张三，2020年从北大计算机硕士毕业，现在在字节跳动做后端开发...\n或者直接粘贴旧简历的文本内容...",
            )
            convert_btn = gr.Button("智能转换", variant="primary", size="lg")
            convert_output = gr.Textbox(
                label="生成的标准 Markdown（可编辑后复制到「生成简历」使用）",
                lines=15,
                interactive=True,
            )

            convert_btn.click(
                fn=convert_raw_content,
                inputs=[convert_input, convert_file, convert_api_key, convert_base_url, convert_model],
                outputs=[convert_output],
            )

        with gr.Tab("AI 润色"):
            gr.Markdown(
                """
### 使用大模型智能优化简历内容

支持任何兼容 OpenAI 格式的 API（如 OpenAI、DeepSeek、智谱、月之暗面等）
"""
            )
            with gr.Row():
                with gr.Column():
                    llm_api_key = gr.Textbox(
                        label="API Key",
                        type="password",
                        placeholder="sk-...",
                    )
                    llm_base_url = gr.Textbox(
                        label="API Base URL",
                        value="https://api.openai.com/v1",
                        placeholder="https://api.openai.com/v1",
                    )
                    llm_model = gr.Textbox(
                        label="模型名称",
                        value="gpt-4o-mini",
                        placeholder="gpt-4o-mini",
                    )
                with gr.Column():
                    llm_md_file = gr.File(
                        label="上传 Markdown 文件",
                        file_types=[".md", ".markdown", ".txt"],
                    )

            llm_input_text = gr.Textbox(
                label="简历 Markdown 内容（可直接编辑）",
                lines=10,
                placeholder="粘贴或上传你的简历 Markdown...",
            )
            polish_btn = gr.Button("AI 润色", variant="primary")
            llm_output_text = gr.Textbox(
                label="润色后的内容（可复制到「生成简历」使用）",
                lines=12,
                interactive=True,
            )

            polish_btn.click(
                fn=polish_with_llm,
                inputs=[llm_md_file, llm_input_text, llm_api_key, llm_base_url, llm_model],
                outputs=[llm_output_text],
            )

        with gr.Tab("帮助 & 示例"):
            gr.Markdown(
                """
## Markdown 格式说明

```markdown
# 姓名

- 手机: 138-0000-0000
- 邮箱: example@email.com
- GitHub: github.com/username
- 地址: 北京市

## 教育经历

### 北京大学 | 计算机科学 | 硕士 | 2020-2023

- GPA: 3.9/4.0
- 相关课程: 机器学习、分布式系统

## 工作经历

### 字节跳动 | 高级后端工程师 | 2023-至今

- 设计并搭建推荐服务，日均处理 1000 万 QPS
- 带领 5 人团队负责内容审核平台

## 项目经历

### 开源简历工具 | github.com/user/repo

- 基于 Python + Gradio 开发的 Web 应用
- 支持多模板和一页自适应

## 技能

- **编程语言**: Python, Go, Java, TypeScript
- **框架**: FastAPI, Django, React
- **工具**: Docker, Kubernetes, Redis
```

## 规则

- `#` 开头 = 姓名
- 列表项（`-`）在第一个 `##` 之前 = 联系方式
- `##` = 大段落标题（教育经历、工作经历、项目、技能等）
- `###` = 具体条目，用 `|` 分隔信息（机构 | 角色 | 时间）
- 列表项在 `###` 下方 = 条目详情
"""
            )
            with gr.Row():
                example_btn_zh = gr.Button("加载中文示例")
                example_btn_en = gr.Button("加载英文示例")
            example_output = gr.Textbox(label="示例内容（可复制使用）", lines=15)

            example_btn_zh.click(
                fn=lambda: load_example("中文示例"),
                outputs=[example_output],
            )
            example_btn_en.click(
                fn=lambda: load_example("英文示例"),
                outputs=[example_output],
            )


if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)
