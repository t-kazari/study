import logging

# ロガーの初期化
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("employee_management")


def get_logger():
    """アプリケーション共通ロガーの取得"""
    return logger
