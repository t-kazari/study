# システム全体アーキテクチャ・設計解説

本システムは、現場の実開発で広く採用されている**クリーンアーキテクチャ（レイヤードアーキテクチャ）**と**コンポーネント指向フロントエンド**を組み合わせた構成になっています。

---

## 1. 全体構成図

```mermaid
flowchart LR
    subgraph Browser["ブラウザ (受講者 / ユーザー)"]
        UI["Next.js 画面 (React / MUI)"]
    end

    subgraph Docker["Docker Compose 実行環境"]
        subgraph FrontendContainer["フロントエンド (Cloud Run 想定)"]
            Next["Next.js (Port: 3000)<br>Pages Router / Emotion"]
        end

        subgraph BackendContainer["バックエンド (Cloud Run 想定)"]
            FastAPI["FastAPI (Port: 8000)<br>Python / uv"]
            DI["Injector (DIコンテナ)"]
        end

        subgraph DBContainer["データベース (Cloud SQL 想定)"]
            MySQL[("MySQL 8.0 (Port: 3306)<br>employee_db")]
        end
    end

    UI -->|HTTP / localhost:3000| Next
    Next -->|axios リバースプロキシ| FastAPI
    FastAPI --> DI
    FastAPI -->|SQLAlchemy| MySQL
```

---

## 2. バックエンドのクリーンアーキテクチャ（レイヤー構造）

バックエンド（FastAPI）は、責任の分離（SoC）とテスト容易性・保守性を高めるため、以下の6つのレイヤーに分割されています。

```mermaid
flowchart TD
    Client["クライアント (Next.js)"] --> Handler["① Handler (Web層 / コントローラー)<br>HTTPリクエスト受付 / バリデーション / HTTPレスポンス"]
    Handler --> Service["② Usecase (Service層 / ビジネスロジック)<br>業務ルール / 重複チェック / トランザクション"]
    Service --> RepoInterface["③ Repository (抽象層 / インターフェース)<br>抽象基底クラス (ABC)"]
    RepoImpl["④ Infra (実装層)<br>SQLAlchemy / MySQL アクセス具象実装"] -.->|実装・バインド| RepoInterface
    Service --> Domain["⑤ Domain (エンティティ / スキーマ)<br>Pydantic モデル / 定数"]
    RepoImpl --> Domain

    DI["⑥ Injector Module (DI層)<br>抽象と具象を結びつける"] -.->|注入| Service
```

### 各ディレクトリの役割

| ディレクトリ | 役割 | 現場での意図 |
| :--- | :--- | :--- |
| `domain/` | 業務データモデル（Pydanticスキーマ）および定数の定義 | 入出力データの形式やビジネスルール上の定数（部署一覧など）を集約する。 |
| `handler/` | FastAPIのルーター（エンドポイント）定義 | URLパスとHTTPメソッド（GET/POST/PUT/DELETE）を定義し、リクエストパラメータを受け取ってServiceを呼び出し、レスポンスを返す。 |
| `usecase/` | ビジネスロジック（`EmployeeService`） | 「メールアドレスが重複していないか」「指定IDの社員が存在するか」などの業務ルールを検証・処理する。 |
| `repository/` | データアクセスの抽象インターフェース（抽象クラス） | DB操作の仕様（メソッド一覧）のみを定義し、特定のDB製品（MySQL等）に依存させない。 |
| `infra/` | Repositoryインターフェースの具象実装（SQLAlchemy） | 実際にMySQLとSQLAlchemyを使ってSQLを発行・実行する。DB製品が変更されてもUsecase層には影響を与えない。 |
| `injectormodule/` | 依存性の注入（DI: Dependency Injection）設定 | `injector` ライブラリを使い、抽象（`EmployeeRepository`）に対して具象（`EmployeeRepositoryImpl`）を自動的に紐付ける。 |
| `utils/` | 共通ログ・コンテキストユーティリティ | アプリケーション全体で使うロガーなどを提供する。 |

---

## 3. なぜ DI（依存性の注入）を使うのか？

バックエンドでは Python の `injector` ライブラリを採用しています。

```python
# injectormodule/di.py
class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        # 抽象インターフェースに対して具象クラスをバインド
        binder.bind(EmployeeRepository, to=EmployeeRepositoryImpl, scope=singleton)
```

### メリット
1. **結合度の低下**: `EmployeeService` は `EmployeeRepository`（抽象）にしか依存していません。MySQLの実装詳細（SQLAlchemy）を知る必要がありません。
2. **単体テストの容易さ**: テスト時には、モック用のInMemoryリポジトリを差し替えるだけで、DBを立ち上げずにServiceのテストを実行できます。

---

## 4. フロントエンドの設計（Next.js + MUI）

フロントエンドは Next.js の **Pages Router** を採用し、Material UI (MUI) と Emotion によるSSR完全対応の構成になっています。

```
frontend/employee-management/
├── pages/
│   ├── _app.tsx              # Emotion CacheProvider と MUI ThemeProvider を包括
│   ├── _document.tsx          # サーバーサイドでEmotionのスタイルタグを抽出・注入
│   ├── index.tsx              # ルートページ
│   ├── EmployeeManagementUi.tsx # 社員管理のメイン画面（ステート管理・API連携）
│   └── components/
│       ├── EmployeeSearchForm.tsx        # 検索条件入力・新規登録ボタン
│       ├── EmployeeTable.tsx             # 一覧テーブル・チェックボックス行内編集・削除ボタン
│       ├── EmployeeCreateModal.tsx       # 新規登録モーダル (React Hook Form + Yup)
│       └── EmployeeDeleteConfirmDialog.tsx # 物理削除確認ダイアログ
├── src/
│   ├── createEmotionCache.ts  # Emotion SSRキャッシュ生成
│   └── theme.js               # MUI カラーテーマ設定
├── types/
│   └── employee.ts            # TypeScript型定義
└── services/
    └── employeeApi.ts         # axios を使ったバックエンドAPI通信関数群
```

### ポイント
- **MUI + Emotion**: GoogleのMaterial Designに基づいた洗練されたUIコンポーネント群を導入。
- **React Hook Form + Yup**: フォームの入力値管理・バリデーションスキーマの分離。
- **axios サービス層**: コンポーネント内に直接 `axios.get` などを散乱させず、`services/employeeApi.ts` にAPI通信を集約。
