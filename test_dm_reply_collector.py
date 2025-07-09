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