# 社員名簿管理システム OJTハンズオン学習教材

本教材は、新卒・新人エンジニアが実際の現場（実開発）で用いられているアーキテクチャ、ディレクトリ構成、ライブラリを用いて、実践的なCRUD Webアプリケーション開発を習得するためのOJT用学習教材です。

---

## 🎯 研修のゴールと身につくスキル

1. **実務レベルのシステム構造の理解**
   - **Frontend**: Next.js (Pages Router) + TypeScript + MUI (Material UI) + Emotion + React Hook Form + Yup + axios
   - **Backend**: FastAPI + SQLAlchemy + MySQL + `injector` によるクリーンアーキテクチャ（DI設計）
2. **Webアプリケーションの一連の流れの体得**
   - ブラウザでの入力・バリデーション → HTTP/REST APIリクエスト送信 → サーバーサイドでのリクエスト検証・DI・ビジネスロジック → ORMによるDB操作（MySQL） → レスポンス返却 → UIの状態更新
3. **チーム開発・実務の作法の習得**
   - Gitブランチ運用（機能ごとの作業、模範解答との差分確認、レビュー）
   - Docker Compose を利用した環境差分のない開発体験

---

## 🌳 Gitブランチ構成と進め方

本リポジトリは以下のブランチ構成で運用します。

| ブランチ名 | 役割 |
| :--- | :--- |
| `main` | 初期状態のデフォルトブランチ |
| **`学習教材_メイン`** | **受講者が最初にチェックアウトする教材の起点ブランチ**（設計書ドキュメントと骨組みコード・TODOコメントを配置） |
| **`画面開発_〇〇`** | **受講者が `学習教材_メイン` から切って作業を進めるブランチ**（例: `画面開発_yamada`） |
| **`画面開発_模範解答`** | **完成版（模範解答）の完全なソースコードが入っているブランチ**（差分確認・レビュー参照用） |

### 進行の流れ
1. `学習教材_メイン` ブランチから、自分の作業ブランチ `画面開発_〇〇` を作成して切り替えます。
   ```bash
   git checkout 学習教材_メイン
   git checkout -b 画面開発_あなたの名前
   ```
2. `docs/assignments/` 配下の課題設計書（Step 1 〜 Step 4）を順番に読みながら、ソースコード内の `TODO` コメント箇所を実装していきます。
3. すべての課題が完成すると、あなたの作業ブランチは `画面開発_模範解答` ブランチと同じ状態になります！詰まったときは `git diff 画面開発_模範解答` で模範解答との差分を確認できます。

---

## 🛠️ 環境構築・起動手順

### 前提条件
- **Docker Desktop** がインストールされ、起動していること
- **Git** がインストールされていること

### 起動コマンド
プロジェクトルート（本リポジトリの直下）でターミナルを開き、以下のコマンドを実行します。

```bash
# 全コンテナ（MySQL, FastAPI, Next.js）をビルドして起動
docker compose up -d --build
```

### 起動確認とアクセス先
コンテナが正常に起動したら、ブラウザで以下のURLを開いて確認してください。

- **🖥️ フロントエンド画面 (Next.js)**: [http://localhost:3000](http://localhost:3000)
- **⚙️ バックエンドAPI Swagger UI (FastAPI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **🩺 バックエンドヘルスチェック**: [http://localhost:8000/health](http://localhost:8000/health)
- **🗄️ MySQL 接続情報 (ローカルGUIツール等で接続する場合)**:
  - ホスト: `127.0.0.1` / ポート: `3306`
  - ユーザー: `user` / パスワード: `password`
  - データベース: `employee_db`
  - ※起動時に `mysql/init.sql` によって初期テーブルと5名のサンプルデータが自動投入されます。

### コンテナの停止・リセット
```bash
# 停止
docker compose down

# DBデータを完全に初期化して再起動したい場合
docker compose down -v
docker compose up -d --build
```

---

## 📚 課題一覧（4ステップ）

各課題の詳細は `docs/assignments/` 配下の各仕様書を参照してください。

- **[課題1: 社員一覧表示・検索機能](./docs/assignments/step1_list.md)**
  - バックエンド: `GET /api/employees`（キーワード・部署絞り込み）のRepository/Usecase/Handler実装
  - フロントエンド: axios による一覧取得と MUI Table による一覧表示・検索機能
- **[課題2: 新規登録モーダル・バリデーション](./docs/assignments/step2_create.md)**
  - バックエンド: `POST /api/employees`（重複チェック・DB登録）の実装
  - フロントエンド: MUI Dialog + React Hook Form + Yup バリデーションフォームの実装
- **[課題3: 行内編集・チェックボックス活性化制御](./docs/assignments/step3_update.md)**
  - バックエンド: `PUT /api/employees/{id}`（社員情報更新）の実装
  - フロントエンド: チェックボックス連動による行内入力欄・保存ボタンの活性化/非活性制御
- **[課題4: 削除機能](./docs/assignments/step4_delete.md)**
  - バックエンド: `DELETE /api/employees/{id}`（物理削除）の実装
  - フロントエンド: 各行の削除ボタン・削除確認ダイアログ・一覧再取得

---

## 📂 ドキュメント目次
- [システム全体アーキテクチャ・設計解説](./docs/system_architecture.md)
- [データベース定義書 (MySQL)](./docs/db_schema.md)
- [課題1 仕様書](./docs/assignments/step1_list.md)
- [課題2 仕様書](./docs/assignments/step2_create.md)
- [課題3 仕様書](./docs/assignments/step3_update.md)
- [課題4 仕様書](./docs/assignments/step4_delete.md)
