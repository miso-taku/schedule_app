"""スケジュール管理アプリケーションのインターフェースとデータモデル。

このモジュールはスケジュール管理システム全体で使用される
抽象インターフェースとPydanticモデルを定義しています。
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    """新しいスケジュールを作成するためのPydanticモデル。
    
    属性:
        title: スケジュールのタイトル。
        description: スケジュールの説明（オプション）。
        start_time: スケジュールの開始時刻。
        end_time: スケジュールの終了時刻。
    """
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime


class ScheduleUpdate(BaseModel):
    """既存のスケジュールを更新するためのPydanticモデル。
    
    部分的な更新を可能にするため、すべてのフィールドはオプションです。
    
    属性:
        title: スケジュールの新しいタイトル。
        description: スケジュールの新しい説明。
        start_time: スケジュールの新しい開始時刻。
        end_time: スケジュールの新しい終了時刻。
        is_completed: スケジュールが完了しているかどうか。
    """
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_completed: Optional[bool] = None


class ScheduleResponse(BaseModel):
    """スケジュールレスポンス用のPydanticモデル。
    
    このモデルはすべてのフィールドを持つ完全なスケジュールを表します。
    
    属性:
        id: スケジュールの一意識別子。
        title: スケジュールのタイトル。
        description: スケジュールの説明。
        start_time: スケジュールの開始時刻。
        end_time: スケジュールの終了時刻。
        is_completed: スケジュールが完了しているかどうか。
        created_at: スケジュールが作成された日時。
        updated_at: スケジュールが最後に更新された日時。
    """
    id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScheduleRepositoryInterface(ABC):
    """スケジュールデータの永続化操作のための抽象インターフェース。
    
    このインターフェースは永続ストレージシステムでスケジュールデータを
    管理するために必要なメソッドを定義します。
    """
    
    @abstractmethod
    def create(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        """リポジトリに新しいスケジュールを作成します。
        
        引数:
            schedule_data: 作成するスケジュールデータ。
            
        戻り値:
            作成されたスケジュールレスポンス。
        """
        pass

    @abstractmethod
    def get_by_id(self, schedule_id: int) -> Optional[ScheduleResponse]:
        """IDによってスケジュールを取得します。
        
        引数:
            schedule_id: 取得するスケジュールのID。
            
        戻り値:
            見つかった場合はスケジュールレスポンス、そうでなければNone。
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        """ページネーション付きですべてのスケジュールを取得します。
        
        引数:
            skip: スキップするスケジュール数。
            limit: 返すスケジュールの最大数。
            
        戻り値:
            スケジュールレスポンスのリスト。
        """
        pass

    @abstractmethod
    def update(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        """既存のスケジュールを更新します。
        
        引数:
            schedule_id: 更新するスケジュールのID。
            update_data: 更新データ。
            
        戻り値:
            見つかった場合は更新されたスケジュールレスポンス、そうでなければNone。
        """
        pass

    @abstractmethod
    def delete(self, schedule_id: int) -> bool:
        """IDによってスケジュールを削除します。
        
        引数:
            schedule_id: 削除するスケジュールのID。
            
        戻り値:
            スケジュールが削除された場合はTrue、見つからなかった場合はFalse。
        """
        pass


class ScheduleServiceInterface(ABC):
    """スケジュールビジネスロジック操作のための抽象インターフェース。
    
    このインターフェースはスケジュール管理のためのビジネスロジックメソッドを定義します。
    リポジトリ層のファサードとして機能します。
    """
    
    @abstractmethod
    def create_schedule(self, schedule_data: ScheduleCreate) -> ScheduleResponse:
        """新しいスケジュールを作成します。
        
        引数:
            schedule_data: 作成するスケジュールデータ。
            
        戻り値:
            作成されたスケジュールレスポンス。
        """
        pass

    @abstractmethod
    def get_schedule(self, schedule_id: int) -> Optional[ScheduleResponse]:
        """IDによってスケジュールを取得します。
        
        引数:
            schedule_id: 取得するスケジュールのID。
            
        戻り値:
            見つかった場合はスケジュールレスポンス、そうでなければNone。
        """
        pass

    @abstractmethod
    def get_schedules(self, skip: int = 0, limit: int = 100) -> List[ScheduleResponse]:
        """ページネーション付きですべてのスケジュールを取得します。
        
        引数:
            skip: スキップするスケジュール数。
            limit: 返すスケジュールの最大数。
            
        戻り値:
            スケジュールレスポンスのリスト。
        """
        pass

    @abstractmethod
    def update_schedule(self, schedule_id: int, update_data: ScheduleUpdate) -> Optional[ScheduleResponse]:
        """既存のスケジュールを更新します。
        
        引数:
            schedule_id: 更新するスケジュールのID。
            update_data: 更新データ。
            
        戻り値:
            見つかった場合は更新されたスケジュールレスポンス、そうでなければNone。
        """
        pass

    @abstractmethod
    def delete_schedule(self, schedule_id: int) -> bool:
        """IDによってスケジュールを削除します。
        
        引数:
            schedule_id: 削除するスケジュールのID。
            
        戻り値:
            スケジュールが削除された場合はTrue、見つからなかった場合はFalse。
        """
        pass