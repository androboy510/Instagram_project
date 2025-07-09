import os
import shutil
import tempfile
from instagram_session import InstagramSession

def test_session_dir_creation_and_check():
    # 임시 디렉토리로 세션 경로 지정
    temp_dir = tempfile.mkdtemp()
    try:
        session = InstagramSession(user_data_dir=temp_dir)
        session.create_session_dir()
        assert os.path.exists(temp_dir)
        # 로그인 상태는 실제로는 수동 확인이지만, 여기서는 항상 False로 가정
        assert session.is_logged_in() is False
    finally:
        shutil.rmtree(temp_dir) 