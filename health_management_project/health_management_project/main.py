# AI 종류: ChatGPT
# AI 사용 목적: 주차 과제 예시와 같은 콘솔 메뉴 및 모듈 1·2 연결
# 사용한 프롬프트: 여기 모듈2를 완성하는데 과제 양식에 맞게 코드를 보내줘
# 사용한 사람: 장태현 / 사용 날짜: 2026-11-24
"""12주차 건강정보 관리 콘솔 프로그램."""

import csv
import pickle
from pathlib import Path

from modules.health_db import load_rows, save_records
from modules.health_logic import HealthManager

DATA_FILE = Path(__file__).resolve().parent / "data" / "health_data.json"
ERRORS = (OSError, ValueError, TypeError, KeyError, EOFError, csv.Error,
          pickle.UnpicklingError)

MENU = """
------------ 건강정보 관리 시스템 ------------
1. 추가
2. 목록 조회
3. 검색 및 상세조회
4. 수정 및 삭제
5. 통계조회
6. 파일에서 가져오기 (모듈1)
7. 파일로 저장 (모듈1)
0. 종료
"""


def read_fields(record=None):
    """입력값을 읽는다. 수정할 때 빈 입력은 이전 값을 사용한다."""
    fields = []
    prompts = ("이름", "출생 연도", "성별(남/여)", "키(cm)", "몸무게(kg)")
    keys = ("name", "birth_year", "gender", "height", "weight")
    for prompt, key in zip(prompts, keys):
        previous = str(getattr(record, key)) if record else ""
        hint = f" [{previous}]" if record else ""
        fields.append(input(f"{prompt}{hint}: ").strip() or previous)
    return fields


def display(records):
    if not records:
        print("조회 결과가 없습니다.")
        return
    print("식별번호 | 이름 | 생년 | 성별 | 키(cm) | 체중(kg) | BMI | 상태")
    for r in records:
        print(f"{r.id} | {r.name} | {r.birth_year} | {r.gender} | "
              f"{r.height:.2f} | {r.weight:.2f} | {r.bmi:.2f} | {r.status}")


def edit_or_delete(manager):
    record = manager.get_record(input("식별번호: "))
    display([record])
    action = input("1. 수정 / 2. 삭제 / 0. 취소: ").strip()
    if action == "1":
        manager.update_record(record.id, *read_fields(record))
        return "수정"
    if action == "2" and input("삭제하려면 y 입력: ").strip().lower() == "y":
        manager.delete_record(record.id)
        return "삭제"
    return ""


def file_path():
    value = input("파일 경로 (Enter = 기본 JSON): ").strip()
    return Path(value).expanduser() if value else DATA_FILE


def show_statistics(manager):
    result = manager.statistics()
    print(f"총 레코드 수: {result['count']}명")
    if result["count"]:
        for field, label in (("height", "키(cm)"), ("weight", "몸무게(kg)"), ("bmi", "BMI")):
            data = result[field]
            print(f"{label} | 평균 {data['mean']:.2f} | 표준편차 {data['std']:.2f}")


def main():
    manager = HealthManager()
    try:
        manager.import_rows(load_rows(DATA_FILE))
    except FileNotFoundError:
        print("저장된 데이터가 없어 빈 목록으로 시작합니다.")
    except ERRORS as error:
        print(f"기본 파일 읽기 실패. 빈 목록으로 시작합니다: {error}")

    while True:
        print(MENU)
        try:
            choice = input("메뉴 선택: ").strip()
            if choice == "0":
                return
            if choice == "1":
                record = manager.add_record(*read_fields())
                print(f"추가 완료: {record.id}")
            elif choice == "2":
                display(manager.list_records())
            elif choice == "3":
                display(manager.search(input("이름, 식별번호 또는 BMI 상태: ")))
            elif choice == "4":
                action = edit_or_delete(manager)
                if action:
                    print(f"{action} 완료")
            elif choice == "5":
                show_statistics(manager)
            elif choice == "6":
                path = file_path()
                mode = input("1. 불러온 목록으로 교체 / 2. 기존 목록에 추가: ").strip()
                if mode not in ("1", "2"):
                    raise ValueError("1 또는 2를 입력하세요.")
                count = manager.import_rows(load_rows(path), append=mode == "2")
                print(f"{count}건 가져오기 완료")
            elif choice == "7":
                path = file_path()
                save_records(path, manager.list_records())
                print(f"저장 완료: {path}")
            else:
                print("메뉴 번호를 다시 입력하세요.")
        except (EOFError, KeyboardInterrupt):
            print("\n프로그램을 종료합니다.")
            return
        except ERRORS as error:
            print(f"처리할 수 없습니다: {error}")


if __name__ == "__main__":
    main()
