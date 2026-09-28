import logging
from typing import Optional
import databases

# ロガーの初期化
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("employee_management")


def get_logger():
    """アプリケーション共通ロガーの取得"""
    return logger


class Context:
    """リクエストや処理のコンテキストオブジェクト（DB接続などを保持）"""

    def __init__(self, db: Optional[databases.Database] = None):
        # 循環インポートを避けるため遅延インポート
        if db is None:
            from employee_management import config
            self.db = config.database
        else:
            self.db = db
