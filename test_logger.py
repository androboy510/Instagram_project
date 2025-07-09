from logger import Logger

def test_log_and_error(tmp_path):
    log_file = tmp_path / "test.log"
    logger = Logger(str(log_file))
    logger.log("info", "테스트 로그")
    logger.log("error", "에러 발생")
    with open(log_file, encoding="utf-8") as f:
        lines = f.readlines()
    assert "[INFO]" in lines[0]
    assert "테스트 로그" in lines[0]
    assert "[ERROR]" in lines[1]
    assert "에러 발생" in lines[1] 