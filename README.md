# 인스타그램 DM 자동화 및 답장 수집 프로젝트

## 프로젝트 목적
- 구글 시트에 입력된 [받는 사람 인스타그램 아이디, 보낼 메시지] 목록을 읽어와서 인스타그램 웹을 통해 자동으로 DM(다이렉트 메시지)을 발송합니다.
- 이후, 상대방이 보낸 답장을 다시 읽어서 구글 시트에 자동으로 기록/정리합니다.

---

## 주요 기능
1. **구글 시트에서 DM 대상 및 메시지 읽기**
2. **Playwright를 통한 인스타그램 DM 자동 발송**
3. **DM 답장(수신 메시지) 자동 수집**
4. **수신된 답장을 구글 시트에 자동 기록**

---

## 사용 기술 및 언어
- **Python**: 전체 자동화 스크립트 작성
- **Playwright**: 웹 브라우저 자동화 (로그인 세션 재사용, DM 발송, 메시지 읽기)
- **Google Sheets API**: 구글 시트 데이터 읽기/쓰기
- **gspread**: Python에서 구글 시트 연동
- **dotenv** (선택): 환경변수 관리

---

## 환경 설정 및 준비 사항

### 1. Python 환경 준비
```bash
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install playwright gspread google-auth python-dotenv
playwright install
```

### 2. 구글 시트 API 설정
1. [Google Cloud Console](https://console.cloud.google.com/)에서 새 프로젝트 생성
2. Google Sheets API 및 Google Drive API 활성화
3. 서비스 계정 생성 및 JSON 키 파일 다운로드
4. 구글 시트 문서를 서비스 계정 이메일에 **공유** (편집 권한)

### 3. 구글 시트 구조 예시
| username | message | reply |
|----------|---------|-------|
| user1    | 안녕하세요 |       |
| user2    | 테스트   |       |

- `username`: DM을 보낼 인스타그램 아이디
- `message`: 보낼 메시지
- `reply`: 받은 답장 (자동 기록)

### 4. Playwright 로그인 세션 준비
- **Playwright로 인스타그램 로그인은 반드시 사용자가 직접 수동으로 해야 합니다.**
- 자동 로그인을 지원하지 않으며, 보안을 위해 사용자가 직접 브라우저에서 로그인해야 합니다.
- Playwright로 브라우저를 실행한 뒤, 직접 인스타그램에 로그인합니다.
- 로그인 후 세션(쿠키 등)을 저장하여 이후 자동화에서 재사용합니다.
- 예시:
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(user_data_dir="./user_data", headless=False)
    page = browser.new_page()
    page.goto("https://instagram.com")
    print("브라우저에서 직접 인스타그램에 로그인하세요. 로그인 완료 후 Enter를 누르세요.")
    input("로그인 후 Enter를 누르세요...")
    browser.close()
```

---

## 실행 방법
1. `.env` 파일에 필요한 환경변수(구글 시트 ID, 서비스 계정 키 경로 등) 설정
2. Playwright로 로그인 세션 준비(최초 1회)
3. 메인 스크립트 실행
```bash
python main.py
```

---

## 주의사항
- 인스타그램 자동화는 계정 정지/제한 위험이 있으니, 너무 빠른 반복 실행을 피하고, 사람처럼 자연스럽게 동작하도록 딜레이를 추가하세요.
- 구글 시트 API 사용 시, 서비스 계정에 시트 공유가 되어 있어야 합니다.
- 인스타그램 UI가 변경되면 자동화 코드도 함께 수정해야 할 수 있습니다.

---

## 폴더 구조 예시
```
Instagram_project/
├── main.py
├── README.md
├── .env
├── user_data/           # Playwright 세션 데이터
├── requirements.txt
```

---

## 참고 자료
- [Playwright 공식 문서](https://playwright.dev/python/)
- [gspread 공식 문서](https://gspread.readthedocs.io/)
- [Google Sheets API Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)

---

## 문의
궁금한 점이나 오류 발생 시, 이슈를 남겨주세요. 

---

## 보안 안내
- 구글 서비스 계정 키 파일(`service_account.json`)은 반드시 `.gitignore`에 추가하여 깃허브에 커밋/푸시되지 않도록 하세요.
- API 키, 비밀키 등 민감한 정보는 절대 공개 저장소에 올리지 마세요. 