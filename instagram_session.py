import os

class InstagramSession:
    def __init__(self, user_data_dir="user_data"):
        self.user_data_dir = user_data_dir

    def create_session_dir(self):
        os.makedirs(self.user_data_dir, exist_ok=True)

    def is_logged_in(self):
        # 실제로는 Playwright로 인스타그램에 접속해 세션 쿠키 등으로 확인해야 함
        # 여기서는 TDD를 위해 항상 False 반환 (실제 구현 시 Playwright 연동)
        return False 