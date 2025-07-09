class DMReplyCollector:
    def __init__(self, playwright):
        self.playwright = playwright

    def collect_replies(self):
        # 실제로는 playwright로 DM 답장 수집
        return self.playwright.collect_replies() 