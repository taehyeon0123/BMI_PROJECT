# AI 종류: ChatGPT
# AI 사용 목적: 모듈 2의 건강정보 CRUD, 검색, 중복 검사, BMI 및 통계 구현
# 사용한 프롬프트: 여기 모듈2를 완성하는데 과제 양식에 맞게 코드를 보내줘
# 사용한 사람: 장태현 / 사용 날짜: 2026-11-24
"""모듈 2. 메모리에서 건강정보를 관리하며 결과를 반환한다."""

from dataclasses import replace
from datetime import date
from math import isfinite
from statistics import mean, pstdev

from .health_db import HealthRecord, ID_PATTERN, next_id


class HealthManager:
    """HealthRecord 목록을 관리한다. 입력과 출력은 호출자가 담당한다."""

    def __init__(self):
        self._records = []

    def list_records(self):
        return [replace(record) for record in self._records]

    def get_record(self, record_id):
        for record in self._records:
            if record.id == record_id.strip().upper():
                return replace(record)
        raise ValueError("해당 식별번호가 없습니다.")

    def search(self, keyword):
        term = keyword.strip().casefold()
        return [
            record for record in self.list_records()
            if term in record.name.casefold()
            or term == record.id.casefold()
            or term == record.status.casefold()
        ]

    def _make_record(self, record_id, name, birth_year, gender, height, weight):
        """입력값을 확인하고 BMI와 판정값을 계산한다."""
        name = name.strip()
        if not name:
            raise ValueError("이름을 입력하세요.")
        birth_year = int(birth_year)
        if not 1 <= birth_year <= date.today().year:
            raise ValueError("올바른 출생 연도를 입력하세요.")
        gender = gender.strip()
        if gender not in ("남", "여"):
            raise ValueError("성별은 남 또는 여로 입력하세요.")
        height, weight = float(height), float(weight)
        if any(not isfinite(value) or value <= 0 for value in (height, weight)):
            raise ValueError("키와 몸무게는 0보다 큰 숫자여야 합니다.")
        try:
            bmi = weight / (height / 100) ** 2
        except (OverflowError, ZeroDivisionError):
            raise ValueError("키와 몸무게의 범위를 확인하세요.") from None
        if not isfinite(bmi) or bmi <= 0:
            raise ValueError("BMI를 계산할 수 있는 범위를 입력하세요.")
        if bmi < 18.5:
            status = "저체중"
        elif bmi < 23:
            status = "정상"
        elif bmi < 25:
            status = "과체중"
        else:
            status = "비만"
        return HealthRecord(record_id, name, birth_year, gender, height, weight,
                            round(bmi, 2), status)

    def _check_duplicate(self, record, exclude_id=None):
        for old in self._records:
            if old.id == exclude_id:
                continue
            same_person = (old.name.casefold(), old.birth_year, old.gender) == (
                record.name.casefold(), record.birth_year, record.gender
            )
            if old.id == record.id or same_person:
                raise ValueError("이미 등록된 식별번호 또는 개인정보입니다.")

    def add_record(self, name, birth_year, gender, height, weight, record_id=""):
        record_id = record_id.strip().upper() or next_id(self._records)
        if not ID_PATTERN.fullmatch(record_id):
            raise ValueError("식별번호는 P2026-0001과 같은 형식이어야 합니다.")
        record = self._make_record(record_id, name, birth_year, gender, height, weight)
        self._check_duplicate(record)
        self._records.append(record)
        return replace(record)

    def update_record(self, record_id, name, birth_year, gender, height, weight):
        old = self.get_record(record_id)
        record = self._make_record(old.id, name, birth_year, gender, height, weight)
        self._check_duplicate(record, exclude_id=old.id)
        self._records[self._records.index(old)] = record
        return replace(record)

    def delete_record(self, record_id):
        record = self.get_record(record_id)
        self._records.remove(record)
        return record

    def import_rows(self, rows, append=False):
        """전체 행을 검사한 뒤 한 번에 반영한다."""
        incoming = HealthManager()
        if append:
            incoming._records = self.list_records()
        for row in rows:
            incoming.add_record(row["name"], row["birth_year"], row["gender"],
                                row["height"], row["weight"], row.get("id") or "")
        self._records = incoming._records
        return len(rows)

    def statistics(self):
        result = {"count": len(self._records)}
        for field in ("height", "weight", "bmi"):
            values = [getattr(record, field) for record in self._records]
            result[field] = {
                "mean": mean(values) if values else None,
                "std": pstdev(values) if values else None,
            }
        return result
