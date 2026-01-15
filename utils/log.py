import logging
import os
from pathlib import Path

from concurrent_log_handler import ConcurrentRotatingFileHandler


class Log(logging.Logger):
    """
    日志配置
    """

    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    FORMATTER: str = "%(asctime)s <%(process)d> [%(levelname)s] [%(filename)s] [lines:%(lineno)s] %(message)s"

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            super(Log, self).__init__("agents", level=logging.INFO)
            self.handlers = []
            self.addHandler(self.file_handler())
            self.addHandler(self.console_handler())
            self._initialized = True

    @staticmethod
    def file_handler():
        """
        文件格式打印日志
        :return:
        """
        base_dir = Path(__file__).resolve(strict=True).parent.parent
        if not os.path.exists("%s/logs" % base_dir):
            os.makedirs("%s/logs" % base_dir)
        path = os.path.join(base_dir, "logs", "agents.log")
        file_handler = ConcurrentRotatingFileHandler(
            path, mode="a", maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter(Log.FORMATTER, datefmt=Log.DATETIME_FORMAT)
        )
        return file_handler

    @staticmethod
    def console_handler():
        """
        控制台输出日志
        :return:
        """
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter(Log.FORMATTER, datefmt=Log.DATETIME_FORMAT)
        )
        return console_handler
