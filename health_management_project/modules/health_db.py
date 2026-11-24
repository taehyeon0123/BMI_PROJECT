# AI 종류: ChatGPT
# AI 사용 목적: 모듈1의 데이터 구조, ID 생성, 파일 입출력 구현 도움
# 사용한 AI 프롬프트:
# "과제 7페이지 모듈1과 11페이지 ID 형식을 참고해서
# 이해하기 쉬운 수준의 파이썬 코드로 알려줘."
# 사용자: 장태현
# 사용 날짜: 2026-11-16

import json
import csv
import pickle
import os
from datetime import datetime


# 파일에 저장할 항목과 순서
FIELDS = []


class HealthRecord:
    """한 사람의 기본 정보와 건강 정보를 저장하는 클래스."""

    def __init__(self, name, birth_year, gender,
                 height, weight, bmi=0.0, status="미계산"):
        """전달받은 정보를 객체에 저장한다."""

        
        self.name = name
        self.birth_year = int(birth_year)
        self.gender = gender
        self.height = float(height)
        self.weight = float(weight)
        self.bmi = float(bmi)
        self.status = status

        if self.height <= 0 or self.weight <= 0:
            raise ValueError("키와 몸무게는 0보다 커야 합니다.")

    def to_dict(self):
        """객체에 저장된 정보를 딕셔너리로 바꾼다."""

        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,      
            "weight": self.weight,
            "bmi": self.bmi,
            "status": self.status
        }


class HealthManager:
    """건강정보 목록, ID 생성, 파일 저장과 불러오기를 담당한다."""

    def __init__(self):
        """빈 목록과 ID 번호를 준비한다."""

        self.records = []
        self.last_number = 0

        # health_db.py가 있는 modules 폴더
        module_folder = os.path.dirname(os.path.abspath(__file__))

        # modules 폴더의 상위인 프로젝트 폴더
        project_folder = os.path.dirname(module_folder)

        # 프로젝트 안의 data 폴더
        self.data_folder = os.path.join(project_folder, "data")
    
    def generate_id(self):
        """올해 연도와 순번으로 새 ID를 만든다."""

        year = datetime.now().year
        prefix = f"P{year}-"

        # 불러온 기존 자료의 ID 번호를 확인한다.
        for record in self.records:
            if record.id.startswith(prefix):
                number = int(record.id[len(prefix):])

                if number > self.last_number:
                    self.last_number = number

        self.last_number += 1

        return f"{prefix}{self.last_number:04d}"

    def save(self, file_type):
        """목록을 지정한 형식으로 저장한다. 성공하면 True를 반환한다."""

        try:
            if file_type not in ["json", "csv", "txt", "pkl"]:
                raise ValueError("지원하지 않는 파일 형식입니다.")

            # data 폴더가 없으면 만든다.
            os.makedirs(self.data_folder, exist_ok=True)

            filename = "health_data." + file_type
            path = os.path.join(self.data_folder, filename)

            # 건강정보 객체를 딕셔너리 목록으로 바꾼다.
            data = []

            for record in self.records:
                data.append(record.to_dict())

            if file_type == "json":
                with open(path, "w", encoding="utf-8") as file:
                    json.dump(
                        data,
                        file,
                        ensure_ascii=False,
                        indent=4
                    )

            elif file_type == "csv" or file_type == "txt":
                with open(
                    path, "w", encoding="utf-8", newline=""
                ) as file:
                    writer = csv.DictWriter(
                        file, fieldnames=FIELDS
                    )

                    # CSV에는 첫 줄에 항목 이름을 넣는다.
                    # TXT에는 항목 이름 없이 자료만 넣는다.
                    if file_type == "csv":
                        writer.writeheader()

                    writer.writerows(data)

            elif file_type == "pkl":
                with open(path, "wb") as file:
                    pickle.dump(self.records, file)

            print(filename, "저장 완료")
            return True

        except Exception as error:
            print("저장 실패:", error)
            return False

    def load(self, file_type):
        """파일을 불러온다. 실패하면 빈 리스트를 반환한다."""

        try:
            if file_type not in ["json", "csv", "txt", "pkl"]:
                raise ValueError("지원하지 않는 파일 형식입니다.")

            filename = "health_data." + file_type
            path = os.path.join(self.data_folder, filename)

            if file_type == "json":
                with open(path, "r", encoding="utf-8-sig") as file:
                    data = json.load(file)

            elif file_type == "csv" or file_type == "txt":
                with open(
                    path, "r", encoding="utf-8-sig", newline=""
                ) as file:

                    if file_type == "csv":
                        reader = csv.DictReader(file)
                    else:
                        reader = csv.DictReader(
                            file, fieldnames=FIELDS
                        )

                    data = list(reader)

            elif file_type == "pkl":
                with open(path, "rb") as file:
                    saved_records = pickle.load(file)

                data = []

                for record in saved_records:
                    data.append(record.to_dict())

            # 읽은 내용을 건강정보 객체로 복원한다.
            loaded_records = []
            used_ids = []

            for item in data:
                record = HealthRecord(
                    id=item["id"],
                    name=item["name"],
                    birth_year=item["birth_year"],
                    gender=item["gender"],
                    height=item["height"],
                    weight=item["weight"],
                    bmi=item["bmi"],
                    status=item["status"]
                )

                # P연도-번호 형태인지 확인한다.
                parts = record.id.split("-")

                if len(parts) != 2:
                    raise ValueError("ID 형식이 잘못되었습니다.")

                if (
                    len(parts[0]) != 5
                    or not parts[0].startswith("P")
                    or not parts[0][1:].isdigit()
                    or not parts[1].isdigit()
                    or int(parts[1]) < 1
                ):
                    raise ValueError("ID 형식이 잘못되었습니다.")

                if record.id in used_ids:
                    raise ValueError("중복된 ID가 있습니다.")

                used_ids.append(record.id)
                loaded_records.append(record)

            # 모든 자료를 정상적으로 읽은 뒤 목록을 교체한다.
            self.records = loaded_records

            print(filename, "불러오기 완료")
            return self.records

        except FileNotFoundError:
            print("저장된 파일이 없습니다.")
            return []

        except Exception as error:
            print("불러오기 실패:", error)
            return []