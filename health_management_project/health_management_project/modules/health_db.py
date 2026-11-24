# AI 종류: ChatGPT
# AI 사용 목적: 모듈 2 실행에 필요한 레코드, 식별번호, 파일 입출력 구현
# 사용한 프롬프트: 여기 모듈2를 완성하는데 과제 양식에 맞게 코드를 보내줘
# 사용한 사람: 장태현 / 사용 날짜: 2026-11-24
"""모듈 1. 건강정보 레코드와 파일 입출력."""

import csv
import json
import pickle
import re
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

FIELDS = "id name birth_year gender height weight bmi status".split()
ID_PATTERN = re.compile(r"P\d{4}-\d{4,}")


@dataclass
class HealthRecord:
    """한 사람의 건강정보를 담는다."""

    id: str
    name: str
    birth_year: int
    gender: str
    height: float
    weight: float
    bmi: float = 0.0
    status: str = ""

    def to_dict(self):
        return asdict(self)


def next_id(records):
    """올해의 식별번호 중 가장 큰 일련번호 다음 번호를 만든다."""
    prefix = f"P{date.today().year}-"
    numbers = [int(r.id.split("-")[1]) for r in records if r.id.startswith(prefix)]
    return f"{prefix}{max(numbers, default=0) + 1:04d}"


class RecordUnpickler(pickle.Unpickler):
    """기본 자료형과 건강정보 레코드만 복원한다."""

    def find_class(self, module, name):
        if module in (__name__, "health_db", "__main__") and name == "HealthRecord":
            return HealthRecord
        raise pickle.UnpicklingError("지원하지 않는 객체가 들어 있습니다.")


def load_rows(filename):
    """JSON, CSV, TXT, PKL을 읽고 레코드 딕셔너리 목록을 반환한다."""
    path = Path(filename)
    suffix = path.suffix.lower()
    if suffix == ".pkl":
        with path.open("rb") as file:
            rows = RecordUnpickler(file).load()
    elif suffix in (".json", ".csv", ".txt"):
        with path.open(encoding="utf-8-sig", newline="") as file:
            if suffix == ".json":
                rows = json.load(file)
            elif suffix == ".csv":
                rows = list(csv.DictReader(file))
            else:
                rows = [dict(zip(FIELDS, row, strict=True))
                        for row in csv.reader(file) if row]
    else:
        raise ValueError("지원하는 형식은 JSON, CSV, TXT, PKL입니다.")
    if not isinstance(rows, list):
        raise ValueError("파일 내용은 레코드 목록이어야 합니다.")
    result = [row.to_dict() if isinstance(row, HealthRecord) else row for row in rows]
    if any(not isinstance(row, dict) for row in result):
        raise ValueError("레코드 형식이 올바르지 않습니다.")
    return result


def save_records(filename, records):
    """레코드 목록을 지정한 형식으로 저장한다."""
    path = Path(filename)
    suffix = path.suffix.lower()
    if suffix not in (".json", ".csv", ".txt", ".pkl"):
        raise ValueError("지원하는 형식은 JSON, CSV, TXT, PKL입니다.")
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    try:
        if suffix == ".pkl":
            with temp.open("wb") as file:
                pickle.dump(records, file)
        else:
            with temp.open("w", encoding="utf-8", newline="") as file:
                if suffix == ".json":
                    json.dump([r.to_dict() for r in records], file,
                              ensure_ascii=False, indent=2)
                else:
                    writer = csv.DictWriter(file, fieldnames=FIELDS)
                    if suffix == ".csv":
                        writer.writeheader()
                    writer.writerows(r.to_dict() for r in records)
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)
