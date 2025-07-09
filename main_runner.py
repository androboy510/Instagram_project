class MainRunner:
    def __init__(self, dm_sender, dm_reply_collector):
        self.dm_sender = dm_sender
        self.dm_reply_collector = dm_reply_collector

    def run(self):
        # DM 발송 및 답장 수집을 순차적으로 실행
        dm_result = self.dm_sender.send_dm("user1", "테스트 메시지")
        replies = self.dm_reply_collector.collect_replies()
        return {"dm": dm_result, "replies": replies} 