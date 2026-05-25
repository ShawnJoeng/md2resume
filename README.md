# md2resume

**Markdown + 证件照 → 精美简历**（PDF / HTML / PNG）

一款开源的智能简历生成工具，支持 AI 智能转换（STAR 法则）、多套专业模板、一页自适应。

## Features

- **AI 智能转换** — 随意粘贴经历/旧简历，AI 自动整理为 STAR 法则格式的专业简历
- **4 套精美模板** — 经典单栏、现代双栏、极简风格、专业风格（高密度排版）
- **一页自适应** — 自动调整间距和字号，让简历恰好填满一页 A4
- **智能加粗** — 关键数据自动加粗突出，每条 bullet 带小标题快速扫描
- **AI 润色** — 接入任意兼容 OpenAI 格式的 API，一键优化措辞
- **多格式导出** — 同时输出 PDF、HTML、PNG
- **中英文支持** — 内置中英文字体栈

## Quick Start

### 1. 安装依赖

```bash
git clone https://github.com/ShawnJoeng/md2resume.git
cd md2resume

pip install -r requirements.txt

# PDF 渲染需要 Playwright（推荐）或 WeasyPrint
pip install playwright
playwright install chromium
```

### 2. 启动应用

```bash
python app.py
```

浏览器打开 `http://localhost:7860` 即可使用。

## 使用流程

### 方式一：智能转换（推荐）

1. 打开「智能转换」Tab
2. 填入你的 API Key 和 Base URL（兼容 OpenAI 格式）
3. 模型选择 `claude-sonnet-4-6`（推荐）或其他强模型
4. 粘贴你的原始经历（任意格式：旧简历、笔记、工作总结等）
5. 点击「智能转换」，AI 会自动整理为 STAR 法则格式
6. 复制生成的 Markdown 到「生成简历」Tab
7. 选择模板（推荐「专业风格」），点击生成

### 方式二：手写 Markdown

按照下方格式规则直接撰写 Markdown，在「生成简历」Tab 上传或粘贴即可。

## Markdown 格式规则

```markdown
# 姓名

- 手机: 138-0000-0000
- 邮箱: example@email.com
- 地址: 北京市

## 教育经历

### 北京大学 | 计算机科学 | 硕士 | 2020-2023 | GPA 3.9/4.0（前5%），国家奖学金

## 工作经历

### 字节跳动 | 后端工程部 高级工程师 | 2023-至今

- 一句话总结这段经历的核心价值
- **推荐系统优化**：针对推荐延迟高的问题，重构缓存架构并引入向量检索，将P99延迟从**200ms**降至**50ms**，日均服务**1000万**QPS
- **团队管理**：带领**5人**团队负责内容审核平台，从0到1完成系统设计到上线，审核效率提升**60%**

## 项目经历

### 开源简历工具 | 个人项目 | 2024.01-2024.03

- **核心功能开发**：基于 Python + Gradio 开发 Web 应用，支持多模板和一页自适应
- **AI 集成**：接入 LLM API 实现智能转换和润色，STAR 法则自动格式化

## 技能

- **编程语言**: Python, Go, Java, TypeScript
- **框架**: FastAPI, Django, React
- **工具**: Docker, Kubernetes, Redis
```

### 格式速查

| 语法 | 含义 |
|------|------|
| `# 标题` | 姓名 |
| `- 项目` (在第一个 `##` 前) | 联系方式 |
| `## 标题` | 段落分类（教育经历/工作经历/项目经历/技能） |
| `### A \| B \| C \| D \| E` | 条目标题，字段用 `\|` 分隔 |
| `- 列表项` (在 `###` 下) | 条目详情（建议 STAR 格式 + **加粗**关键数据） |

### STAR 法则写 bullet

每条工作/项目 bullet 遵循：

```
- **小标题**：[背景/问题] + [你的行动]，[**量化结果**]
```

示例：
- **自动评估系统**：针对模型迭代依赖高成本人工评测的问题，设计多维度评估框架并搭建自动化系统，效率提升**98.81%**

## 模板说明

| 模板 | 特点 | 适合场景 |
|:----:|:----:|:--------:|
| 经典单栏 | 传统专业布局 | 传统行业、国企 |
| 现代双栏 | 侧边栏 + 主内容区 | 互联网/技术 |
| 极简风格 | 大留白、衬线字体 | 创意/学术 |
| 专业风格 | 高密度紧凑排版 | 内容丰富、需要一页展示大量经历 |

## AI 模型推荐

支持任何兼容 OpenAI API 格式的服务：

| 服务商 | Base URL | 推荐模型 |
|--------|----------|----------|
| Anthropic (推荐) | 兼容 OpenAI 格式的中转 | claude-sonnet-4-6 |
| OpenAI | `https://api.openai.com/v1` | gpt-4o |
| DeepSeek | `https://api.deepseek.com` | deepseek-chat |
| 智谱 AI | `https://open.bigmodel.cn/api/paas/v4` | glm-4-flash |

> 智能转换功能对模型能力要求较高，推荐使用 Claude Sonnet 4 或 GPT-4o 级别模型。

## Tech Stack

- **前端**: [Gradio](https://gradio.app/)
- **PDF 渲染**: [Playwright](https://playwright.dev/) + Chromium / [WeasyPrint](https://weasyprint.org/)
- **模板引擎**: [Jinja2](https://jinja.palletsprojects.com/)
- **PNG 转换**: [PyMuPDF](https://pymupdf.readthedocs.io/)
- **LLM**: [OpenAI Python SDK](https://github.com/openai/openai-python)（兼容格式）

## License

MIT
