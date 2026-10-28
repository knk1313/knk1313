"""README の年齢と学年を今日の日付（JST）から更新する。"""

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

BIRTHDAY = (2005, 2, 7)
ENROLLED_YEAR = 2023  # 学部入学年度（4月入学）
GRADES = ["B1", "B2", "B3", "B4", "M1", "M2"]

README = Path(__file__).resolve().parent.parent / "README.md"


def calc_age(today):
    y, m, d = BIRTHDAY
    return today.year - y - ((today.month, today.day) < (m, d))


def calc_grade(today):
    fiscal_year = today.year if today.month >= 4 else today.year - 1
    index = fiscal_year - ENROLLED_YEAR
    return GRADES[min(index, len(GRADES) - 1)]


def replace(text, tag, value):
    return re.sub(rf"(<!--{tag}-->).*?(<!--/{tag}-->)", rf"\g<1>{value}\g<2>", text)


def main():
    today = datetime.now(timezone(timedelta(hours=9))).date()
    text = README.read_text(encoding="utf-8")
    text = replace(text, "age", calc_age(today))
    text = replace(text, "grade", calc_grade(today))
    README.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
