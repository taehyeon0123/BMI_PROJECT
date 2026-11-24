# 12주차 지정개인 과제 — BMI 건강관리 프로그램

제출자 장태현

프로젝트 폴더에서 Python 3.10 이상으로 `python3 main.py`를 실행합니다.
건강정보 관리 로직은 `modules/health_logic.py`, 레코드 구조와 파일 입출력은
`modules/health_db.py`, 콘솔 화면은 `main.py`에 있습니다.

- 시작할 때 `data/health_data.json`을 읽습니다.
- 메뉴 6에서 파일을 불러오거나 현재 목록에 합칩니다. 엑셀 자료는 헤더가 포함된 CSV로 저장해 가져옵니다. 새 레코드의 ID는 비워 둘 수 있습니다.
- 추가·수정·삭제 결과를 파일에 반영하려면 메뉴 7로 저장합니다. Enter를 누르면 기본 JSON 파일에 저장합니다.
- 표준편차는 현재 등록된 전체 레코드를 모집단으로 계산합니다.
- BMI 분류 기준은 18.5, 23, 25를 경계로 사용합니다. 판정 후 BMI를 소수 둘째 자리로 표시합니다.

CSV 헤더는 `id,name,birth_year,gender,height,weight,bmi,status`입니다.
`bmi`와 `status`는 가져올 때 자동 계산합니다.
