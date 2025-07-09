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