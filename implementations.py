"""スケジュール管理インターフェースの具体的実装。

このモジュールはリポジトリとサービスインターフェースの
具体的実装、およびSQLAlchemyデータベースモデルを含んでいます。"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List, Optional
from interfaces import (
    ScheduleCreate, 
    ScheduleUpdate, 
    ScheduleResponse, 
    ScheduleRepositoryInterface, 
    ScheduleServiceInterface
)


DATABASE_URL = "sqlite:///./schedule.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Schedule(Base):
    """schedulesテーブル用のSQLAlchemyモデル。
    
    このモデルはデータベース内のスケジュールレコードを表します。
    
    属性:
        id: 主キー識別子。
        title: スケジュールのタイトル。
        description: スケジュールのオプション説明。
        start_time: スケジュールの開始時刻。
        end_time: スケジュールの終了時刻。
        is_completed: スケジュールが完了しているかどうか。
        created_at: スケジュールが作成されたタイムスタンプ。
        updated_at: スケジュールが最後に更新されたタイムスタンプ。
    """
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ScheduleRepository(ScheduleRepositoryInterface):
    """スケジュールリポジトリインターフェースの具体的実装。
    
    このクラスはSQLAlchemyを使用してスケジュールのデータ永続化操作を提供します。
    """
    
    def __init__(self):
        """リポジトリを初期化し、データベーステーブルを作成します。"""
        Base.metadata.create_all(bind=engine)

    def _get_db(self) -> Session:
        """データベースセッションを取得します。
        
        戻り値:
            SQLAlchemyデータベースセッション。
        """
        return SessionLocal()

    def create(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        """データベースに新しいスケジュールを作成します。
        
        引数:
            schedule_data: 作成するスケジュールデータ。
            
        戻り値:
            作成されたスケジュールレスポンス。
        """
        db = self._get_db()
        try:
            db_schedule = Schedule(**schedule_data.dict())
            db.add(db_schedule)
            db.commit()
            db.refresh(db_schedule)
            return ScheduleResponse.from_orm(db_schedule)
        finally:
            db.close()

    def get_by_id(self, schedule_id: int) -> Optional[ScheduleResponse]:
        """データベースからIDによってスケジュールを取得します。
        
        引数:
            schedule_id: 取得するスケジュールのID。
            
        戻り値:
            見つかった場合はスケジュールレスポンス、そうでなければNone。
        """
        db = self._get_db()
        try:
            schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if schedule:
                return ScheduleResponse.from_orm(schedule)
            return None
        finally:
            db.close()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        """データベースからページネーション付きですべてのスケジュールを取得します。
        
        引数:
            skip: スキップするスケジュール数。
            limit: 返すスケジュールの最大数。
            
        戻り値:
            スケジュールレスポンスのリスト。
        """
        db = self._get_db()
        try:
            schedules = db.query(Schedule).offset(skip).limit(limit).all()
            return [ScheduleResponse.from_orm(schedule) for schedule in schedules]
        finally:
            db.close()

    def update(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        """データベース内の既存のスケジュールを更新します。
        
        引数:
            schedule_id: 更新するスケジュールのID。
            update_data: 更新データ。
            
        戻り値:
            見つかった場合は更新されたスケジュールレスポンス、そうでなければNone。
        """
        db = self._get_db()
        try:
            schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if not schedule:
                return None
            
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(schedule, field, value)
            
            schedule.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(schedule)
            return ScheduleResponse.from_orm(schedule)
        finally:
            db.close()

    def delete(self, schedule_id: int) -> bool:
        """データベースからスケジュールを削除します。
        
        引数:
            schedule_id: 削除するスケジュールのID。
            
        戻り値:
            スケジュールが削除された場合はTrue、見つからない場合はFalse。
        """
        db = self._get_db()
        try:
            schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if not schedule:
                return False
            
            db.delete(schedule)
            db.commit()
            return True
        finally:
            db.close()


class ScheduleService(ScheduleServiceInterface):
    """スケジュールサービスインターフェースの具体的実装。
    
    このクラスはスケジュールのビジネスロジック操作を提供します。
    リポジトリ層に対するファサードとして機能します。
    """
    
    def __init__(self, repository: ScheduleRepositoryInterface):
        """リポジトリでサービスを初期化します。
        
        引数:
            repository: スケジュールリポジトリの実装。
        """
        self.repository = repository

    def create_schedule(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        """新しいスケジュールを作成します。
        
        引数:
            schedule_data: 作成するスケジュールデータ。
            
        戻り値:
            作成されたスケジュールレスポンス。
        """
        return self.repository.create(schedule_data)

    def get_schedule(self, schedule_id: int) -> Optional[ScheduleResponse]:
        """IDによってスケジュールを取得します。
        
        引数:
            schedule_id: 取得するスケジュールのID。
            
        戻り値:
            見つかった場合はスケジュールレスポンス、そうでなければNone。
        """
        return self.repository.get_by_id(schedule_id)

    def get_schedules(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        """ページネーション付きですべてのスケジュールを取得します。
        
        引数:
            skip: スキップするスケジュール数。
            limit: 返すスケジュールの最大数。
            
        戻り値:
            スケジュールレスポンスのリスト。
        """
        return self.repository.get_all(skip, limit)

    def update_schedule(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        """既存のスケジュールを更新します。
        
        引数:
            schedule_id: 更新するスケジュールのID。
            update_data: 更新データ。
            
        戻り値:
            見つかった場合は更新されたスケジュールレスポンス、そうでなければNone。
        """
        return self.repository.update(schedule_id, update_data)

    def delete_schedule(self, schedule_id: int) -> bool:
        """IDによってスケジュールを削除します。
        
        引数:
            schedule_id: 削除するスケジュールのID。
            
        戻り値:
            スケジュールが削除された場合はTrue、見つからない場合はFalse。
        """
        return self.repository.delete(schedule_id)


def get_db():
    """データベースセッションを取得する依存関数。
    
    この関数はFastAPIの依存関数として使用され、
    エンドポイントにデータベースセッションを提供します。
    
    戻り値:
        SQLAlchemyデータベースセッション。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_schedule_service() -> ScheduleService:
    """スケジュールサービスインスタンスを作成するファクトリ関数。
    
    リポジトリ実装を持つスケジュールサービスを作成します。
    
    戻り値:
        設定されたスケジュールサービスインスタンス。
    """
    repository = ScheduleRepository()
    return ScheduleService(repository)