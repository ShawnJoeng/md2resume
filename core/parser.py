from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class ResumeEntry:
    title: str
    subtitle: str = ""
    date: str = ""
    details: List[str] = field(default_factory=list)


@dataclass
class ResumeData:
    name: str = ""
    contact: Dict[str, str] = field(default_factory=dict)
    photo_base64: str = ""
    sections: Dict[str, List[ResumeEntry]] = field(default_factory=dict)


SECTION_ALIASES = {
    "教育经历": "education",
    "教育背景": "education",
    "学历": "education",
    "education": "education",
    "工作经历": "experience",
    "工作经验": "experience",
    "work experience": "experience",
    "experience": "experience",
    "项目经历": "projects",
    "项目": "projects",
    "projects": "projects",
    "技能": "skills",
    "专业技能": "skills",
    "skills": "skills",
    "获奖": "awards",
    "荣誉": "awards",
    "awards": "awards",
    "honors": "awards",
    "论文": "publications",
    "发表": "publications",
    "publications": "publications",
    "自我评价": "summary",
    "个人简介": "summary",
    "summary": "summary",
    "about": "summary",
}

CONTACT_PREFIXES = {
    "phone": ["phone", "电话", "手机", "tel"],
    "email": ["email", "邮箱", "e-mail"],
    "github": ["github"],
    "linkedin": ["linkedin"],
    "website": ["website", "网站", "个人主页", "blog", "博客"],
    "location": ["location", "地址", "城市", "地点"],
    "wechat": ["wechat", "微信"],
}


def _detect_contact_key(text: str) -> Tuple[str, str]:
    lower = text.lower().strip()
    for key, prefixes in CONTACT_PREFIXES.items():
        for prefix in prefixes:
            if lower.startswith(prefix):
                value = re.sub(r'^[^:：]+[:：]\s*', '', text).strip()
                return key, value
    return "other", text.strip()


def _parse_entry_header(header: str) -> ResumeEntry:
    parts = [p.strip() for p in header.split('|')]
    entry = ResumeEntry(title=parts[0])
    if len(parts) >= 3:
        entry.subtitle = parts[1]
        entry.date = parts[-1]
    elif len(parts) == 2:
        if re.search(r'\d{4}', parts[1]):
            entry.date = parts[1]
        else:
            entry.subtitle = parts[1]
    return entry


def parse_markdown(md_content: str) -> ResumeData:
    lines = md_content.strip().split('\n')
    resume = ResumeData()

    current_section = None
    current_entry = None
    in_header = True

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('# ') and not stripped.startswith('## '):
            resume.name = stripped[2:].strip()
            continue

        if stripped.startswith('## '):
            in_header = False
            if current_entry and current_section is not None:
                resume.sections[current_section].append(current_entry)
                current_entry = None

            section_name = stripped[3:].strip()
            normalized = SECTION_ALIASES.get(section_name.lower(), section_name)
            current_section = section_name
            resume.sections[current_section] = []
            continue

        if stripped.startswith('### '):
            if current_entry and current_section is not None:
                resume.sections[current_section].append(current_entry)
            header_text = stripped[4:].strip()
            current_entry = _parse_entry_header(header_text)
            continue

        if in_header and re.match(r'^[-*]\s+', stripped):
            item_text = re.sub(r'^[-*]\s+', '', stripped)
            key, value = _detect_contact_key(item_text)
            resume.contact[key] = value
            continue

        if re.match(r'^[-*]\s+', stripped) and current_section is not None:
            item_text = re.sub(r'^[-*]\s+', '', stripped)
            if current_entry:
                current_entry.details.append(item_text)
            else:
                entry = ResumeEntry(title=item_text)
                resume.sections[current_section].append(entry)
            continue

        if stripped and current_entry and not stripped.startswith('#'):
            current_entry.details.append(stripped)

    if current_entry and current_section is not None:
        resume.sections[current_section].append(current_entry)

    return resume
