class DMSender:
    def __init__(self, playwright):
        self.playwright = playwright

    def send_dm(self, username, message):
        # 실제로는 playwright로 인스타그램 DM 발송
        # 여기서는 TDD를 위해 DummyPW의 send_dm을 호출
        return self.playwright.send_dm(username, message) 