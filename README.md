# スケジュール管理API

スケジュールとイベントを管理するためのFastAPIベースのREST APIです。

## 機能

- スケジュールの作成、読み取り、更新、削除
- SQLAlchemy ORMを使用したSQLiteデータベース
- 自動データベーステーブル作成
- RESTful APIエンドポイント
- Swagger UIによる組み込みAPI文書

## 要件

- Python >= 3.12
- FastAPI
- SQLAlchemy
- Uvicorn
- Pydantic

## インストール

1. リポジトリをクローンする
2. 依存関係をインストールする:
   ```bash
   pip install fastapi sqlalchemy uvicorn pydantic-settings python-multipart
   ```

## アプリケーションの実行

```bash
python main.py
```

APIは `http://localhost:8000` で利用できます

## API文書

実行後、以下にアクセスしてください:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## APIエンドポイント

- `GET /` - ルートエンドポイント
- `POST /schedules/` - 新しいスケジュールを作成
- `GET /schedules/` - 全てのスケジュールを一覧表示（ページネーション付き）
- `GET /schedules/{id}` - 特定のスケジュールを取得
- `PUT /schedules/{id}` - スケジュールを更新
- `DELETE /schedules/{id}` - スケジュールを削除

## データモデル

各スケジュールには以下が含まれます:
- `id` - 一意識別子
- `title` - スケジュールタイトル（必須）
- `description` - 説明（任意）
- `start_time` - 開始日時
- `end_time` - 終了日時
- `is_completed` - 完了状態
- `created_at` - 作成タイムスタンプ
- `updated_at` - 最終更新タイムスタンプ