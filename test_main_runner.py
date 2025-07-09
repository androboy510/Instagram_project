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