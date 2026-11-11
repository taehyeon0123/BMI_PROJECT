
# AI 활용: ChatGPT
# 목적: 건강정보 클래스 작성 및 학습
# 프롬프트: 이해하고 설명할 수 있는 수준의 모듈 1 코드 작성
# 사용자: [본인 이름]
# 날짜: 2026-11-11

class HealthRecord:

    def __init__(self, name, birth_year, gender, height, weight):

        self.name = name
        self.birth_year = birth_year
        self.gender = gender
        self.height = height
        self.weight = weight

        self.bmi = round(weight / ((height / 100) ** 2), 2)

        if self.bmi < 18.5:
            self.status = "저체중"
        elif self.bmi < 23:
            self.status = "정상"
        elif self.bmi < 25:
            self.status = "과체중"
        else:
            self.status = "비만"

    def to_dict(self):
        return {
                "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "bmi": self.bmi,
            "status": self.status
        }
