# AI 종류: ChatGPT
# AI 사용 목적:
# 모듈1 실행을 위한 팀원 정보 입력 및 파일 저장·불러오기 코드 작성
# 사용한 AI 프롬프트:
# "과제 7페이지 모듈1과 11페이지 ID 형식을 참고하고,
# 제공한 팀원 정보를 넣어서 이해하기 쉬운 코드로 완성해줘."
# 사용자: 장태현
# 사용 날짜: 2026-11-16

from modules.health_db import HealthRecord, HealthManager


# 1. 건강정보를 관리할 객체 만들기
manager = HealthManager()


# 2. 장태현 정보
person1 = HealthRecord(
    id=manager.generate_id(),
    name="장태현",
    birth_year=2004,
    gender="남",
    height=171,
    weight=66,
    bmi=22.57,
    status="정상"
)

manager.records.append(person1)


# 3. 전재균 정보
person2 = HealthRecord(
    id=manager.generate_id(),
    name="전재균",
    birth_year=2002,
    gender="남",
    height=180,
    weight=80,
    bmi=24.69,
    status="과체중"
)

manager.records.append(person2)


# 4. 김기범 정보
person3 = HealthRecord(
    id=manager.generate_id(),
    name="김기범",
    birth_year=2007,
    gender="남",
    height=173,
    weight=70,
    bmi=23.39,
    status="과체중"
)

manager.records.append(person3)


# 5. 최민호 정보
person4 = HealthRecord(
    id=manager.generate_id(),
    name="최민호",
    birth_year=2001,
    gender="남",
    height=172,
    weight=79,
    bmi=26.70,
    status="비만"
)

manager.records.append(person4)


# 6. 입력한 팀원 정보 출력
print("\n===== 팀원 건강정보 =====")

for person in manager.records:
    print(
        f"ID: {person.id} | "
        f"이름: {person.name} | "
        f"생년: {person.birth_year} | "
        f"성별: {person.gender} | "
        f"키: {person.height}cm | "
        f"몸무게: {person.weight}kg | "
        f"BMI: {person.bmi:.2f} | "
        f"상태: {person.status}"
    )

print("총 인원:", len(manager.records), "명")


# 7. 네 가지 파일 형식으로 저장하고 다시 불러오기
file_types = ["json", "csv", "txt", "pkl"]

for file_type in file_types:
    print("\n=====", file_type, "파일 저장 및 불러오기 =====")

    # 저장에 성공했을 때만 불러오기를 진행한다.
    success = manager.save(file_type)

    if success:
        # 빈 관리자를 새로 만들어 파일을 읽는다.
        new_manager = HealthManager()
        loaded_records = new_manager.load(file_type)

        for person in loaded_records:
            print(person.to_dict())

        # 저장 전후의 내용이 같은지 확인한다.
        original_data = []
        loaded_data = []

        for person in manager.records:
            original_data.append(person.to_dict())

        for person in loaded_records:
            loaded_data.append(person.to_dict())

        if original_data == loaded_data:
            print("확인 완료: 저장 전후의 정보가 같습니다.")
        else:
            print("확인 필요: 저장 전후의 정보가 다릅니다.")

    else:
        print("저장에 실패해서 불러오기를 진행하지 않았습니다.")