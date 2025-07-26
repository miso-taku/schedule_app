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
- Googleスタイルのdocstringsによる詳細な文書化

## アーキテクチャ

このプロジェクトは以下の3つのファイルに分離されたクリーンなアーキテクチャを採用しています：

### ファイル構成

- **`main.py`**: FastAPIアプリケーションのエントリーポイントとAPIエンドポイント
- **`interfaces.py`**: データモデル（Pydantic）と抽象インターフェース
- **`implementations.py`**: SQLAlchemyモデルと具体的な実装クラス

### レイヤー構成

```
Presentation Layer (main.py)
    ↓
Business Logic Layer (ScheduleService)
    ↓
Data Access Layer (ScheduleRepository)
    ↓
Data Layer (SQLite Database)
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

1. **インターフェース層** (`interfaces.py`)
   - `ScheduleRepositoryInterface`: データアクセス層の抽象インターフェース
   - `ScheduleServiceInterface`: ビジネスロジック層の抽象インターフェース
   - Pydanticデータモデル（Create, Update, Response）

2. **実装層** (`implementations.py`)
   - `Schedule`: SQLAlchemyモデル
   - `ScheduleRepository`: データアクセスの具体実装
   - `ScheduleService`: ビジネスロジックの具体実装

3. **プレゼンテーション層** (`main.py`)
   - FastAPIアプリケーション
   - HTTPエンドポイント
   - 依存性注入の設定

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
├── main.py              # FastAPIアプリケーションエントリーポイント
├── interfaces.py        # データモデルと抽象インターフェース
├── implementations.py   # SQLAlchemyモデルと実装クラス
├── README.md           # プロジェクト文書
├── .gitignore          # Git除外ファイル
├── pyproject.toml      # uvプロジェクト設定
└── schedule.db         # SQLiteデータベース（実行時に作成）
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。