# スケジュール管理API

スケジュールとイベントを管理するためのFastAPIベースのREST APIです。

## 機能

- スケジュールの作成、読み取り、更新、削除（CRUD操作）
- SQLAlchemy ORMを使用したSQLiteデータベース
- 自動データベーステーブル作成
- RESTful APIエンドポイント
- Swagger UIによる組み込みAPI文書
- クリーンアーキテクチャの採用（インターフェースと実装の分離）
- リポジトリパターンによるデータアクセス層の抽象化
- 詳細設計書による包括的なドキュメント化

## アーキテクチャ

このプロジェクトはクリーンアーキテクチャパターンを採用し、以下の4つのレイヤーに分離されています：

### ディレクトリ構成

```
schedule_app/
├── presentation/           # プレゼンテーション層
│   ├── controllers/       # HTTPリクエスト処理
│   └── routes/           # APIエンドポイント定義
├── application/           # アプリケーション層
│   └── services/         # ビジネスロジック
├── domain/               # ドメイン層
│   ├── entities/         # エンティティとDTO
│   └── repositories/     # リポジトリインターフェース
├── infrastructure/       # インフラストラクチャ層
│   ├── database/        # データベース設定・モデル
│   ├── repositories/    # リポジトリ実装
│   └── dependencies.py  # 依存性注入
└── docs/                # ドキュメント
```

### レイヤー構成

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Presentation  │    │   Application   │    │     Domain      │    │ Infrastructure  │
│     Layer       │────│     Layer       │────│     Layer       │────│     Layer       │
│                 │    │                 │    │                 │    │                 │
│ • Routes        │    │ • Services      │    │ • Entities      │    │ • Database      │
│ • Controllers   │    │                 │    │ • Repositories  │    │ • Repository    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    │   Implementations│
                                                                      └─────────────────┘
```

## 要件

- Python >= 3.12
- uv（Pythonパッケージマネージャー）
- FastAPI
- SQLAlchemy
- Uvicorn
- Pydantic

## インストール

1. リポジトリをクローンする
   ```bash
   git clone <repository-url>
   cd schedule_app
   ```

2. uvをインストール（まだインストールしていない場合）:
   ```bash
   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. プロジェクトの初期化と依存関係のインストール:
   ```bash
   uv init --no-readme
   uv add fastapi sqlalchemy uvicorn pydantic-settings python-multipart
   ```

## アプリケーションの実行

```bash
uv run python main.py
```

または、開発モードで実行する場合:
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

APIは `http://localhost:8000` で利用できます

## API文書

実行後、以下にアクセスしてください:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## APIエンドポイント

| メソッド | エンドポイント | 説明 |
|----------|---------------|------|
| `GET` | `/` | ルートエンドポイント（ウェルカムメッセージ） |
| `POST` | `/schedules/` | 新しいスケジュールを作成 |
| `GET` | `/schedules/` | 全てのスケジュールを一覧表示（ページネーション付き） |
| `GET` | `/schedules/{id}` | 特定のスケジュールを取得 |
| `PUT` | `/schedules/{id}` | スケジュールを更新 |
| `DELETE` | `/schedules/{id}` | スケジュールを削除 |

## データモデル

### ScheduleCreate（作成用）
- `title` (string) - スケジュールタイトル（必須）
- `description` (string, optional) - 説明
- `start_time` (datetime) - 開始日時
- `end_time` (datetime) - 終了日時

### ScheduleUpdate（更新用）
- `title` (string, optional) - スケジュールタイトル
- `description` (string, optional) - 説明
- `start_time` (datetime, optional) - 開始日時
- `end_time` (datetime, optional) - 終了日時
- `is_completed` (boolean, optional) - 完了状態

### ScheduleResponse（レスポンス用）
- `id` (integer) - 一意識別子
- `title` (string) - スケジュールタイトル
- `description` (string) - 説明
- `start_time` (datetime) - 開始日時
- `end_time` (datetime) - 終了日時
- `is_completed` (boolean) - 完了状態
- `created_at` (datetime) - 作成タイムスタンプ
- `updated_at` (datetime) - 最終更新タイムスタンプ

## 使用例

### スケジュールの作成
```bash
curl -X POST "http://localhost:8000/schedules/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "会議",
    "description": "プロジェクト進捗会議",
    "start_time": "2024-01-20T10:00:00",
    "end_time": "2024-01-20T11:00:00"
  }'
```

### スケジュール一覧の取得
```bash
curl -X GET "http://localhost:8000/schedules/?skip=0&limit=10"
```

### 特定スケジュールの取得
```bash
curl -X GET "http://localhost:8000/schedules/1"
```

### スケジュールの更新
```bash
curl -X PUT "http://localhost:8000/schedules/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "更新された会議",
    "is_completed": true
  }'
```

### スケジュールの削除
```bash
curl -X DELETE "http://localhost:8000/schedules/1"
```

## 開発者向け情報

### コードの構造

1. **プレゼンテーション層** (`presentation/`)
   - `routes/schedule_routes.py`: APIエンドポイント定義
   - `controllers/schedule_controller.py`: HTTPリクエスト処理とレスポンス生成

2. **アプリケーション層** (`application/`)
   - `services/schedule_service.py`: ビジネスロジックと抽象インターフェース

3. **ドメイン層** (`domain/`)
   - `entities/schedule.py`: Pydanticデータモデル（Create, Update, Response）
   - `repositories/schedule_repository.py`: リポジトリの抽象インターフェース

4. **インフラストラクチャ層** (`infrastructure/`)
   - `database/models.py`: SQLAlchemyモデル
   - `database/connection.py`: データベース接続設定
   - `repositories/schedule_repository_impl.py`: リポジトリの具体実装
   - `dependencies.py`: 依存性注入の設定

5. **エントリーポイント** (`main.py`)
   - FastAPIアプリケーション設定
   - ルーターの統合

### 拡張性

このアーキテクチャにより、以下の拡張が容易になります：
- 異なるデータベース（PostgreSQL、MySQL等）への変更
- 新しいビジネスロジックの追加
- テストの作成（モックによる単体テスト）
- キャッシュレイヤーの追加
- 認証・認可機能の追加

## 開発とテスト

### 開発環境での実行
```bash
# 開発モードで自動リロード有効
uv run uvicorn main:app --reload
```

### 依存関係の管理
```bash
# 新しいパッケージの追加
uv add <package-name>

# 開発用依存関係の追加
uv add --dev <package-name>

# 依存関係の更新
uv sync

# 仮想環境の確認
uv info
```

### プロジェクト構造
```
schedule_app/
├── main.py                     # FastAPIアプリケーションエントリーポイント
├── presentation/               # プレゼンテーション層
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── schedule_controller.py
│   └── routes/
│       ├── __init__.py
│       └── schedule_routes.py
├── application/                # アプリケーション層
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       └── schedule_service.py
├── domain/                     # ドメイン層
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── schedule.py
│   └── repositories/
│       ├── __init__.py
│       └── schedule_repository.py
├── infrastructure/             # インフラストラクチャ層
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── models.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── schedule_repository_impl.py
│   └── dependencies.py
├── docs/                       # ドキュメント
│   └── 詳細設計書.md
├── README.md                   # プロジェクト文書
├── pyproject.toml             # uvプロジェクト設定
├── uv.lock                    # 依存関係ロックファイル
└── schedule.db                # SQLiteデータベース（実行時に作成）
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。