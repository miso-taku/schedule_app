from application.services.schedule_service import ScheduleService, ScheduleServiceInterface
from infrastructure.repositories.schedule_repository_impl import ScheduleRepositoryImpl


def get_schedule_service() -> ScheduleServiceInterface:
    repository = ScheduleRepositoryImpl()
    return ScheduleService(repository)