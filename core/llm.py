from openai import OpenAI

SYSTEM_PROMPT = """你是一位专业的简历编辑。你的任务是：
1. 让每个要点更简洁有力
2. 使用强动词开头（设计、实现、主导、优化、搭建、推动...）
3. 尽可能量化成果（提升X%、服务XW用户、节省X小时）
4. 去除冗余和填充词
5. 保持输入的语言（中文保持中文，英文保持英文）
6. 保留所有事实信息，绝不捏造

请返回优化后的 Markdown，保持与输入完全相同的结构格式（标题层级、列表符号等）。"""


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
