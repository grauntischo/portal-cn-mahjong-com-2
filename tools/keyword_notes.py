from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# 示例数据：关联页面与关键词
SAMPLE_URL = "https://portal-cn-mahjong.com"
SAMPLE_KEYWORD = "麻将胡了"


@dataclass
class KeywordNote:
    """表示一条关键词笔记的数据类"""
    keyword: str
    source_url: str
    created_at: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    content: str = ""

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "source_url": self.source_url,
            "created_at": self.created_at,
            "tags": self.tags,
            "content": self.content,
        }


@dataclass
class NoteCollection:
    """保存一组关键词笔记的集合"""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword in n.keyword]

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]


def format_note_single(note: KeywordNote) -> str:
    """单条笔记的可读文本输出"""
    lines = [
        f"关键词：{note.keyword}",
        f"来源：{note.source_url}",
        f"创建时间：{note.created_at}",
        f"标签：{'、'.join(note.tags) if note.tags else '无'}",
    ]
    if note.content:
        lines.append(f"内容：{note.content}")
    return "\n".join(lines)


def format_note_markdown(note: KeywordNote) -> str:
    """单条笔记的 Markdown 格式输出"""
    tag_str = ", ".join(note.tags) if note.tags else "无"
    md_lines = [
        f"### {note.keyword}",
        f"- **来源**：{note.source_url}",
        f"- **创建时间**：{note.created_at}",
        f"- **标签**：{tag_str}",
    ]
    if note.content:
        md_lines.append(f"\n{note.content}")
    return "\n".join(md_lines)


def format_collection_summary(collection: NoteCollection) -> str:
    """整个笔记集合的摘要文本"""
    if not collection.notes:
        return "（无笔记）"
    parts = [
        f"共 {len(collection.notes)} 条关键词笔记",
        "=" * 30,
    ]
    for i, note in enumerate(collection.notes, 1):
        parts.append(f"{i}. {note.keyword} —— {note.source_url}  [{', '.join(note.tags)}]")
    return "\n".join(parts)


def demo_usage():
    """演示使用，包含示例数据"""
    note1 = KeywordNote(
        keyword=SAMPLE_KEYWORD,
        source_url=SAMPLE_URL,
        tags=["示例", "游戏术语"],
        content="麻将胡了是游戏中的胜利状态。",
    )
    note2 = KeywordNote(
        keyword="听牌",
        source_url=SAMPLE_URL,
        tags=["麻将", "策略"],
        content="只剩一张牌就能胡牌的状态。",
    )
    note3 = KeywordNote(
        keyword="国士无双",
        source_url="https://example.com/mahjong",
        tags=["特殊牌型"],
        content="一种和牌牌型。",
    )
    collection = NoteCollection()
    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)

    print("=== 格式化输出（单条文本） ===")
    print(format_note_single(note1))
    print()
    print("=== 格式化输出（Markdown） ===")
    print(format_note_markdown(note2))
    print()
    print("=== 集合摘要 ===")
    print(format_collection_summary(collection))
    print()
    print("=== 按关键词筛选 ===")
    for n in collection.filter_by_keyword("胡"):
        print(f"- {n.keyword} ({n.source_url})")
    print()
    print("=== 按标签筛选 ===")
    for n in collection.filter_by_tag("策略"):
        print(f"- {n.keyword} ({n.source_url})")


if __name__ == "__main__":
    demo_usage()