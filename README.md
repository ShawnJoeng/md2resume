# md2resume

**Markdown + 证件照 → 精美简历**（PDF / HTML / PNG）

一款开源的智能简历生成工具，让你用 Markdown 写简历，一键生成专业排版的 PDF。

## Features

- **Markdown 驱动** — 用你最熟悉的格式书写简历内容
- **3 套精美模板** — 经典单栏、现代双栏、极简风格
- **一页自适应** — 自动调整间距和字号，让简历恰好填满一页
- **AI 智能润色** — 接入任意兼容 OpenAI 格式的 API（如 DeepSeek、智谱、月之暗面等），一键优化简历措辞
- **多格式导出** — 同时输出 PDF、HTML、PNG
- **中英文支持** — 内置中英文字体栈，自动适配

## Quick Start

### 1. 安装依赖

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/md2resume.git
cd md2resume

# 安装 Python 依赖
pip install -r requirements.txt

# 安装系统依赖（macOS）
brew install poppler

# Linux (Ubuntu/Debian)
# sudo apt-get install poppler-utils
```

### 2. 启动应用

```bash
python app.py
```

浏览器打开 `http://localhost:7860` 即可使用。

## Markdown 格式

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

### 公司名 | 职位 | 时间段

- 工作内容和成果描述

## 项目经历

### 项目名 | 链接

- 项目描述

## 技能

- **编程语言**: Python, Go, Java
- **框架**: FastAPI, React
```

### 格式规则

| 语法 | 含义 |
|------|------|
| `# 标题` | 姓名 |
| `- 项目` (在第一个 `##` 前) | 联系方式 |
| `## 标题` | 段落分类 |
| `### 内容` | 条目（用 `\|` 分隔多字段） |
| `- 列表项` (在 `###` 下) | 条目详情 |

## 模板预览

| 经典单栏 | 现代双栏 | 极简风格 |
|:--------:|:--------:|:--------:|
| 传统专业布局 | 侧边栏 + 主内容区 | 大留白衬线字体 |
| 适合传统行业 | 适合互联网/技术 | 适合创意/学术 |

## AI 润色

支持任何兼容 OpenAI API 格式的服务：

| 服务商 | Base URL | 推荐模型 |
|--------|----------|----------|
| OpenAI | `https://api.openai.com/v1` | gpt-4o-mini |
| DeepSeek | `https://api.deepseek.com` | deepseek-chat |
| 智谱 AI | `https://open.bigmodel.cn/api/paas/v4` | glm-4-flash |
| 月之暗面 | `https://api.moonshot.cn/v1` | moonshot-v1-8k |

## Tech Stack

- **前端**: [Gradio](https://gradio.app/)
- **PDF 渲染**: [WeasyPrint](https://weasyprint.org/)
- **模板引擎**: [Jinja2](https://jinja.palletsprojects.com/)
- **PNG 转换**: [pdf2image](https://github.com/Belval/pdf2image) + Poppler
- **LLM**: [OpenAI Python SDK](https://github.com/openai/openai-python)

## License

MIT
