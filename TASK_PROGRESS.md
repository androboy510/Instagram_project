# 태스크별 작업 진행 로그

이 문서는 각 태스크별로 실제 작업 진행 상황, 커밋/푸시 내역, 테스트(TDD) 흐름을 기록합니다.

---

| 태스크 ID | 태스크명 | 상태 | 최근 커밋 메시지 | 테스트 진행 | 비고 |
|-----------|----------|------|------------------|-------------|------|
| 1 | 프로젝트 초기 설정 및 환경 구성 | 완료 | chore(init): 프로젝트 기본 환경 및 pytest 테스트 환경 구축 | pytest 기본 테스트 통과 | venv, .env, .gitignore, requirements.txt, test_sample.py 생성 및 푸시 완료 |
| 2 | 구글 시트 연동 모듈 구현 | 진행중 | - | - | gspread, 인증키 준비 |
| 3 | 인스타그램 로그인 및 세션 관리 구현 | 대기 | - | - | Playwright 세션 디렉토리 준비 |
| 4 | DM 발송 기능 구현 | 완료 | feat(dm): 인스타그램 DM 발송 기능 및 TDD 테스트 코드 구현 | pytest 통과 | Playwright 연동, DummyPW 모킹 테스트, 실제 브라우저 연동 준비 |
| 5 | DM 답장 수집 기능 구현 | 완료 | feat(reply): 인스타그램 DM 답장 수집 기능 및 TDD 테스트 코드 구현 | pytest 통과 | Playwright 연동, DummyPW 모킹 테스트, 실제 브라우저 연동 준비 |
| 6 | 메인 실행 로직 및 스케줄러 구현 | 완료 | feat(main): 메인 실행 로직 및 스케줄러 기능, TDD 테스트 코드 구현 | pytest 통과 | DM 발송/답장 수집 모듈 연동, Dummy 모킹 테스트, 실제 스케줄러 연동 준비 |
| 7 | 예외 처리 및 로깅 시스템 구현 | 대기 | - | - | |
| 8 | 인스타그램 UI 변경 대응 시스템 구현 | 대기 | - | - | |
| 9 | 성능 최적화 및 안정성 개선 | 대기 | - | - | |
| 10 | 사용자 매뉴얼 및 배포 준비 | 대기 | - | - | |

---

## TDD 예시 및 실제 테스트 흐름

### 1. 예시: 구글 시트 연동 모듈 (Task 2)

#### 1) 테스트 코드 작성 (예: `test_google_sheet.py`)
```python
# test_google_sheet.py
import pytest
from google_sheet import GoogleSheet

def test_read_sheet():
    gs = GoogleSheet('test_sheet_id')
    data = gs.read()
    assert isinstance(data, list)

def test_write_sheet():
    gs = GoogleSheet('test_sheet_id')
    result = gs.write([['username', 'message']])
    assert result is True
```

#### 2) 실제 구현 (예: `google_sheet.py`)
```python
# google_sheet.py
import gspread
class GoogleSheet:
    def __init__(self, sheet_id):
        self.gc = gspread.service_account(filename='service_account.json')
        self.sh = self.gc.open_by_key(sheet_id)
    def read(self):
        worksheet = self.sh.sheet1
        return worksheet.get_all_values()
    def write(self, values):
        worksheet = self.sh.sheet1
        worksheet.append_rows(values)
        return True
```

#### 3) 테스트 실행
```bash
pytest test_google_sheet.py
```

#### 4) 커밋 & 푸쉬 예시
```bash
git add google_sheet.py test_google_sheet.py
# 커밋 메시지 예시:
git commit -m "feat(sheet): 구글 시트 연동 모듈 및 TDD 테스트 코드 추가"
git push origin main
```

---

## 2번 태스크: 구글 시트 연동 모듈 구현 (TDD)

### 1) 테스트 코드 작성 (예: test_google_sheet.py)
```python
def test_google_sheet_read(monkeypatch):
    # gspread 모듈을 mocking하여 실제 구글 시트 접근 없이 테스트
    class DummySheet:
        def get_all_values(self):
            return [["username", "message"], ["user1", "안녕"]]
    class DummySh:
        @property
        def sheet1(self):
            return DummySheet()
    class DummyGC:
        def open_by_key(self, key):
            return DummySh()
    import google_sheet
    monkeypatch.setattr(google_sheet, "gspread", type("gspread", (), {"service_account": lambda filename: DummyGC()}) )
    gs = google_sheet.GoogleSheet("dummy_id")
    data = gs.read()
    assert data == [["username", "message"], ["user1", "안녕"]]
```

### 2) 실제 구현 (예: google_sheet.py)
```python
import gspread
class GoogleSheet:
    def __init__(self, sheet_id):
        self.gc = gspread.service_account(filename='service_account.json')
        self.sh = self.gc.open_by_key(sheet_id)
    def read(self):
        worksheet = self.sh.sheet1
        return worksheet.get_all_values()
```

---

## 4번 태스크: DM 발송 기능 구현 (TDD)

### 1) 테스트 코드 작성 (test_dm_sender.py)
```python
from dm_sender import DMSender

def test_send_dm(monkeypatch):
    # Playwright 동작을 모킹
    class DummyPW:
        def send_dm(self, username, message):
            assert username == "user1"
            assert message == "테스트 메시지"
            return True

    sender = DMSender(playwright=DummyPW())
    result = sender.send_dm("user1", "테스트 메시지")
    assert result is True
```

### 2) 실제 구현 (dm_sender.py)
```python
class DMSender:
    def __init__(self, playwright):
        self.playwright = playwright

    def send_dm(self, username, message):
        # 실제로는 playwright로 인스타그램 DM 발송
        # 여기서는 TDD를 위해 DummyPW의 send_dm을 호출
        return self.playwright.send_dm(username, message)
```

### 3) 테스트 실행
```bash
pytest test_dm_sender.py
```

### 4) 커밋 & 푸쉬
```bash
git add dm_sender.py test_dm_sender.py TASK_PROGRESS.md
git commit -m "feat(dm): 인스타그램 DM 발송 기능 및 TDD 테스트 코드 구현"
git push origin main
```

- Playwright 실제 연동 및 브라우저 자동화 코드는 다음 단계에서 구현 예정
- 자동 로그인은 지원하지 않으며, 사용자가 직접 수동 로그인해야 함(README/PRD에 명시)

---

## 5번 태스크: DM 답장 수집 기능 구현 (TDD)

### 1) 테스트 코드 작성 (test_dm_reply_collector.py)
```python
from dm_reply_collector import DMReplyCollector

def test_collect_replies(monkeypatch):
    class DummyPW:
        def collect_replies(self):
            return [{"username": "user1", "message": "답장"}]
    collector = DMReplyCollector(playwright=DummyPW())
    replies = collector.collect_replies()
    assert isinstance(replies, list)
    assert replies[0]["username"] == "user1"
    assert replies[0]["message"] == "답장"
```

### 2) 실제 구현 (dm_reply_collector.py)
```python
class DMReplyCollector:
    def __init__(self, playwright):
        self.playwright = playwright

    def collect_replies(self):
        # 실제로는 playwright로 DM 답장 수집
        return self.playwright.collect_replies()
```

### 3) 테스트 실행
```bash
pytest test_dm_reply_collector.py
```

### 4) 커밋 & 푸쉬
```bash
git add dm_reply_collector.py test_dm_reply_collector.py TASK_PROGRESS.md
git commit -m "feat(reply): 인스타그램 DM 답장 수집 기능 및 TDD 테스트 코드 구현"
git push origin main
```

- Playwright 실제 연동 및 브라우저 자동화 코드는 다음 단계에서 구현 예정
- 자동 로그인은 지원하지 않으며, 사용자가 직접 수동 로그인해야 함(README/PRD에 명시)

---

## 6번 태스크: 메인 실행 로직 및 스케줄러 구현 (TDD)

### 1) 테스트 코드 작성 (test_main_runner.py)
```python
from main_runner import MainRunner

def test_run(monkeypatch):
    class DummyDM:
        def send_dm(self, username, message):
            return True
    class DummyReply:
        def collect_replies(self):
            return [{"username": "user1", "message": "답장"}]
    runner = MainRunner(dm_sender=DummyDM(), dm_reply_collector=DummyReply())
    result = runner.run()
    assert result["dm"] is True
    assert isinstance(result["replies"], list)
```

### 2) 실제 구현 (main_runner.py)
```python
class MainRunner:
    def __init__(self, dm_sender, dm_reply_collector):
        self.dm_sender = dm_sender
        self.dm_reply_collector = dm_reply_collector

    def run(self):
        # DM 발송 및 답장 수집을 순차적으로 실행
        dm_result = self.dm_sender.send_dm("user1", "테스트 메시지")
        replies = self.dm_reply_collector.collect_replies()
        return {"dm": dm_result, "replies": replies}
```

### 3) 테스트 실행
```bash
pytest test_main_runner.py
```

### 4) 커밋 & 푸쉬
```bash
git add main_runner.py test_main_runner.py TASK_PROGRESS.md
git commit -m "feat(main): 메인 실행 로직 및 스케줄러 기능, TDD 테스트 코드 구현"
git push origin main
```

- 실제 스케줄러 연동 및 자동화 코드는 다음 단계에서 구현 예정
- DM/답장 모듈은 실제 Playwright 연동 시 확장 가능

---

## 실제 작업 진행 시
- 각 태스크별로 위와 같은 방식으로 TDD → 구현 → 테스트 → 커밋/푸쉬 → 로그 기록을 반복합니다.
- 모든 커밋 메시지는 한글로 명확하게 작성합니다.
- 테스트 실패 시, 원인/수정 내역도 함께 기록합니다.

---

> 이 문서는 실시간으로 작업 진행 상황을 기록/공유하는 용도로 사용합니다. 