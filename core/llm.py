from openai import OpenAI

SYSTEM_PROMPT = """你是一位专业的简历编辑。你的任务是：
1. 让每个要点更简洁有力
2. 使用强动词开头（设计、实现、主导、优化、搭建、推动...）
3. 尽可能量化成果（提升X%、服务XW用户、节省X小时）
4. 去除冗余和填充词
5. 保持输入的语言（中文保持中文，英文保持英文）
6. 保留所有事实信息，绝不捏造

请返回优化后的 Markdown，保持与输入完全相同的结构格式（标题层级、列表符号等）。"""

CONVERT_PROMPT = """你是一位顶尖的简历顾问。用户会提供非结构化的原始内容，你需要将其精炼为一份适合 **1 页 A4** 的专业简历。

## 核心原则：少即是多

这份简历必须在一页内展示最强竞争力。宁可删减，不可啰嗦。

## 严格格式规则

输出会被程序解析，必须遵循：

1. `# 姓名` — 一级标题仅用于姓名
2. `- 前缀: 值` — 第一个 `##` 之前为联系方式
3. `## 段落标题` — 只允许 4 个段落：教育经历、工作经历、项目经历、技能
4. `### 条目` — 三级标题，字段用 `|` 分隔
5. `- 要点` — 一级列表（**禁止缩进/嵌套**）

## 篇幅硬性约束

- 全文总 bullet（`-` 开头的行）控制在 **20-30 条**
- 每个 `###` 条目下 **最多 4 条** bullet
- 每条 bullet **不超过 60 个字**，一句话说完一个成果
- 工作经历：同一公司按方向分为 **2-3 个** `###` 条目
- 项目经历：保留 **2-3 个** 最有代表性的项目，每个项目 2-3 条 bullet
- 教育经历：保留 GPA、排名、研究方向等关键信息
- 荣誉奖项：合并为技能段的一条（如 `- **荣誉**: 攻坚克难奖、闪耀新锐奖、Hackathon黑马奖等6项`）

## 内容筛选优先级

1. 量化成果优先（数字、百分比、排名）
2. 独立主导的工作 > 参与的工作
3. 最近的经历 > 较早的经历
4. 删除所有"目标"、"项目背景"、"项目概况"等描述性文字
5. 删除重复表述（同一成果只出现一次）

## 输出模板

```
# 姓名

- 手机: xxx
- 邮箱: xxx
- 地址: xxx

## 教育经历

### 学校 | 专业 | 学位 | 时间

## 工作经历

### 公司 | 核心职责方向 | 时间

- 量化成果1（不超过50字）
- 量化成果2
- 量化成果3

## 项目经历

### 项目名 | 机构 | 时间

- 一句话说明做了什么和成果

## 技能

- **类别**: 技能列表
- **荣誉**: 奖项列表（合并为一条）
```

## 其他约束

- 绝不捏造信息
- 保持原始语言
- 无姓名则用 [姓名] 占位
- 直接输出 Markdown，无解释、无代码块包裹"""


def refine_resume(
    md_content: str,
    api_key: str,
    base_url: str = "https://api.openai.com/v1",
    model: str = "gpt-4o-mini",
) -> str:
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"请优化以下简历内容：\n\n{md_content}"},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


def convert_to_resume(
    raw_content: str,
    api_key: str,
    base_url: str = "https://api.openai.com/v1",
    model: str = "gpt-4o-mini",
) -> str:
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": CONVERT_PROMPT},
            {"role": "user", "content": f"请将以下内容整理成标准简历 Markdown 格式：\n\n{raw_content}"},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content
