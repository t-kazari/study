# データベース定義書 (MySQL)

本システムで使用するデータベーススキーマおよび初期投入データについての仕様書です。

---

## 1. 接続情報 (ローカルDocker Compose)

| 項目 | 設定値 |
| :--- | :--- |
| **データベース種別** | MySQL 8.0 (InnoDB / utf8mb4) |
| **ホスト** | `mysql` (コンテナ内) / `127.0.0.1` (ホストマシン) |
| **ポート** | `3306` |
| **データベース名** | `employee_db` |
| **ユーザー** | `user` |
| **パスワード** | `password` |
| **ルートパスワード** | `rootpassword` |

---

## 2. テーブル定義: `employees` (社員マスタ)

| カラム名 | データ型 | NULL許容 | キー | 初期値 | 論理名・説明 |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `id` | `INT` | NO | PK | AUTO_INCREMENT | 社員ID（内部主キー） |
| `employee_code` | `VARCHAR(20)` | NO | UNIQUE | - | 社員番号（業務キー、例: `EMP001`） |
| `name` | `VARCHAR(100)` | NO | - | - | 氏名 |
| `email` | `VARCHAR(150)` | NO | UNIQUE | - | メールアドレス |
| `department` | `VARCHAR(50)` | NO | - | - | 所属部署（`開発部`, `営業部`, `人事部`, `総務部`） |
| `position` | `VARCHAR(50)` | NO | - | - | 役職（`一般`, `リーダー`, `マネージャー`, `部長`） |
| `joined_date` | `DATE` | NO | - | - | 入社日（YYYY-MM-DD） |
| `status` | `VARCHAR(20)` | NO | - | `'在籍'` | 在籍ステータス（`在籍`, `休職`, `退職`） |
| `created_at` | `DATETIME` | NO | - | `CURRENT_TIMESTAMP` | レコード作成日時 |
| `updated_at` | `DATETIME` | NO | - | `CURRENT_TIMESTAMP ON UPDATE` | レコード最終更新日時 |

---

## 3. 初期投入サンプルデータ (`mysql/init.sql`)

コンテナ初回起動時に以下の5件のデータが自動投入されます。

| id | employee_code | name | email | department | position | joined_date | status |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| 1 | `EMP001` | 山田 太郎 | `yamada.taro@example.com` | 開発部 | リーダー | 2021-04-01 | 在籍 |
| 2 | `EMP002` | 佐藤 花子 | `sato.hanako@example.com` | 開発部 | 一般 | 2023-04-01 | 在籍 |
| 3 | `EMP003` | 鈴木 一郎 | `suzuki.ichiro@example.com` | 営業部 | マネージャー | 2019-10-01 | 在籍 |
| 4 | `EMP004` | 高橋 健太 | `takahashi.kenta@example.com` | 人事部 | 一般 | 2022-04-01 | 休職 |
| 5 | `EMP005` | 田中 美咲 | `tanaka.misaki@example.com` | 総務部 | 一般 | 2024-04-01 | 在籍 |
