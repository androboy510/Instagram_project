from datetime import datetime

class Logger:
    def __init__(self, log_file="app.log"):
        self.log_file = log_file

    def log(self, level, message):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{now}] [{level.upper()}] {message}\n") 