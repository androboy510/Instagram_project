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