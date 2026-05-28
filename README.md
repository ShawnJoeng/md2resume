# md2resume

**Markdown + 证件照 → 精美简历**（PDF / HTML / PNG）

一款开源的智能简历生成工具，支持 AI 智能转换（STAR 法则）、专业模板、一页自适应。

## Features

- **AI 智能转换** — 随意粘贴经历/旧简历，AI 自动整理为 STAR 法则格式的专业简历
- **专业模板** — 高密度紧凑排版，一页展示大量经历
- **一页自适应** — 自动调整间距和字号，让简历恰好填满一页 A4
- **智能加粗** — 关键数据自动加粗突出，每条 bullet 带小标题快速扫描
- **AI 润色** — 接入任意兼容 OpenAI 格式的 API，一键优化措辞
- **多格式导出** — 同时输出 PDF、HTML、PNG

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
python app.py #或 python3 app.py
```

浏览器打开 `http://localhost:7860` 即可使用。

## 使用流程

1. 填入你的 API Key 和 Base URL（兼容 OpenAI 格式）
2. 粘贴你的原始经历（任意格式：旧简历、笔记、工作总结等）
3. 点击「智能转换」，AI 会自动整理为 STAR 法则格式
4. 上传证件照（可选），点击「生成简历」


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

- **核心功能开发**：基于 Python + Gradio 开发 Web 应用，支持一页自适应
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

使用「专业风格」模板：高密度紧凑排版、蓝色分割线、● 段落图标、工作简介无圆点、关键数据加粗、STAR 法则 bullet。

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

## 示例

以下是一份完整的简历 Markdown 示例，可直接粘贴到工具中生成：

```markdown
# 李明

- 手机: 186-1234-5678
- 邮箱: liming@email.com
- 微信: liming_dev

## 教育经历

### 清华大学 | 计算机科学与技术 | 硕士 | 2019-2022 | GPA 3.8/4.0（前10%），校级优秀毕业生

### 浙江大学 | 软件工程 | 本科 | 2015-2019 | GPA 3.6/4.0，ACM 省赛银牌

## 工作经历

### 阿里巴巴 | 搜索事业部 高级算法工程师 | 2022.07-至今

- 负责搜索排序算法优化与大规模分布式系统架构设计
- **排序模型升级**：针对搜索相关性不足的问题，设计多目标融合排序框架并落地 Transformer 模型，搜索点击率提升**12%**，GMV 增长**8%**
- **实时特征平台**：主导搭建实时特征计算平台，支撑**5000万**日活用户的个性化搜索，特征时效性从小时级优化至**秒级**
- **向量检索引擎**：从0到1构建基于 HNSW 的向量检索服务，支持**10亿**级别向量库，P99 延迟**<15ms**

### 腾讯 | 微信支付 后端开发工程师 | 2021.06-2022.06（实习）

- 参与微信支付核心链路性能优化
- **支付链路优化**：分析慢查询瓶颈并重构数据库索引策略，核心接口 TP99 从**800ms**降至**200ms**
- **容灾方案设计**：设计多机房主备切换方案，故障切换时间从**5分钟**缩短至**30秒**

## 项目经历

### 智能客服对话系统 | 阿里内部项目 | 2023.03-2023.09

- **意图识别模块**：基于 BERT 微调实现多轮对话意图分类，准确率达**94.5%**，覆盖**200+**业务场景
- **知识库检索**：结合 RAG 架构实现企业知识库问答，回答准确率**85%**，人工介入率降低**40%**

### 开源贡献 | Apache Flink Contributor | 2020-2022

- **窗口算子优化**：优化 Session Window 合并逻辑，大窗口场景性能提升**3x**，PR 被合入主分支

## 技能

- **编程语言**: Python, Java, C++, Go
- **机器学习**: PyTorch, TensorFlow, Transformers, LangChain
- **大数据**: Flink, Spark, Kafka, Elasticsearch
- **基础设施**: Kubernetes, Docker, Redis, MySQL
- **语言**: 英语 CET-6 590 分，可流畅阅读论文和技术文档
```

生成效果为一页 A4 专业简历，包含紧凑排版、关键数据加粗、STAR 法则格式。
