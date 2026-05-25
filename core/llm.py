from openai import OpenAI

SYSTEM_PROMPT = """你是一位专业的简历编辑。你的任务是：
1. 让每个要点更简洁有力
2. 使用强动词开头（设计、实现、主导、优化、搭建、推动...）
3. 尽可能量化成果（提升X%、服务XW用户、节省X小时）
4. 去除冗余和填充词
5. 保持输入的语言（中文保持中文，英文保持英文）
6. 保留所有事实信息，绝不捏造

请返回优化后的 Markdown，保持与输入完全相同的结构格式（标题层级、列表符号等）。"""

CONVERT_PROMPT = """你是一位专业的简历整理专家。用户会提供一段非结构化的原始内容（可能是随意写的经历描述、旧简历文本、聊天记录、笔记等）。

你的任务是将其整理成以下标准 Markdown 简历格式：

```
# 姓名

- 手机: xxx
- 邮箱: xxx
- GitHub: xxx（如有）
- 地址: xxx（如有）

## 教育经历

### 学校名 | 专业 | 学位 | 起止时间

- 具体描述

## 工作经历

### 公司名 | 职位 | 起止时间

- 工作成果和职责描述

## 项目经历

### 项目名 | 简短说明

- 项目描述

## 技能

- **类别**: 具体技能列表
```

要求：
1. 从用户的原始内容中提取所有可用信息，按上述结构组织
2. 如果某个段落的信息不足，仍然保留该段落，但内容可以简短
3. 如果无法判断某信息属于哪个类别，合理归类
4. 保持原始语言（中文输入输出中文，英文输入输出英文）
5. 绝不捏造任何信息——只整理和重组用户提供的内容
6. 用简洁有力的语言重写描述，使用动词开头
7. 如果用户没有提供姓名或联系方式，用占位符 [姓名]、[联系方式] 标记

直接返回整理好的 Markdown，不要有任何额外解释。"""


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
