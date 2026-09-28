"""ドメイン定数定義モジュール"""
import os

# SecretManagerから取得・マウントされたCloud SQL接続情報のJSONパス
DB_SECRET_PATH = os.getenv("DB_SECRET_PATH", "/etc/secrets/cloud_sql.json")

# 所属部署の定義
DEPARTMENTS = ["開発部", "営業部", "人事部", "総務部"]

# 役職の定義
POSITIONS = ["一般", "リーダー", "マネージャー", "部長"]

# 在籍ステータスの定義
STATUSES = ["在籍", "休職", "退職"]
