from typing import List, Optional

from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist

from api.models import Incident, Status, Source


class StatusRepository:
    @staticmethod
    def get_default_status() -> Status:
        try:
            return Status.objects.get(code="open")
        except Status.DoesNotExist:
            StatusRepository.create_default_statuses()
            return Status.objects.get(code="open")

    @staticmethod
    def create_default_statuses():
        """Создать стандартные статусы"""
        default_statuses = [
            {"code": "open", "name": "Открыт", "order": 0},
            {"code": "in_progress", "name": "В работе", "order": 1},
            {"code": "resolved", "name": "Решен", "order": 2},
            {"code": "closed", "name": "Закрыт", "order": 3},
        ]
        for status_data in default_statuses:
            Status.objects.get_or_create(code=status_data["code"], defaults=status_data)

    @staticmethod
    def get_status_by_code(code: str) -> Optional[Status]:
        try:
            return Status.objects.get(code=code, is_active=True)
        except Status.DoesNotExist:
            return None

    @staticmethod
    def get_all_statuses() -> QuerySet[Status]:
        return Status.objects.filter(is_active=True).order_by("order")

    @staticmethod
    def get_available_statuses() -> List[dict]:
        statuses = StatusRepository.get_all_statuses()
        return [{"value": status.code, "label": status.name} for status in statuses]


class SourceRepository:
    @staticmethod
    def get_default_source() -> Source:
        try:
            return Source.objects.get(code="operator")
        except Source.DoesNotExist:
            SourceRepository.create_default_sources()
            return Source.objects.get(code="operator")

    @staticmethod
    def create_default_sources():
        """Создать стандартные источники"""
        default_sources = [
            {"code": "operator", "name": "Оператор"},
            {"code": "monitoring", "name": "Мониторинг"},
            {"code": "partner", "name": "Партнер"},
        ]
        for source_data in default_sources:
            Source.objects.get_or_create(code=source_data["code"], defaults=source_data)

    @staticmethod
    def get_source_by_code(code: str) -> Optional[Source]:
        try:
            return Source.objects.get(code=code, is_active=True)
        except Source.DoesNotExist:
            return None

    @staticmethod
    def get_all_sources() -> QuerySet[Source]:
        return Source.objects.filter(is_active=True).order_by("name")

    @staticmethod
    def get_available_sources() -> List[dict]:
        sources = SourceRepository.get_all_sources()
        return [{"value": source.code, "label": source.name} for source in sources]


class IncidentRepository:
    @staticmethod
    def get_all_incidents() -> QuerySet[Incident]:
        return Incident.objects.select_related("status", "source").all()

    @staticmethod
    def get_incidents_by_status(status_code: str) -> QuerySet[Incident]:
        return Incident.objects.select_related("status", "source").filter(
            status__code=status_code, status__is_active=True
        )

    @staticmethod
    def get_incident_by_id(incident_id: int) -> Optional[Incident]:
        try:
            return Incident.objects.select_related("status", "source").get(
                id=incident_id
            )
        except Incident.DoesNotExist:
            return None

    @staticmethod
    def create_incident(
        description: str, source_code: str, status_code: str = None
    ) -> Incident:
        if not description.strip():
            raise ValueError("Description cannot be empty")

        source = SourceRepository.get_source_by_code(source_code)
        if source is None:
            source = SourceRepository.get_default_source()

        if status_code:
            status = StatusRepository.get_status_by_code(status_code)
            if status is None:
                status = StatusRepository.get_default_status()
        else:
            status = StatusRepository.get_default_status()

        return Incident.objects.create(
            description=description.strip(), source=source, status=status
        )

    @staticmethod
    def update_incident_status(
        incident_id: int, status_code: str
    ) -> Optional[Incident]:
        incident = IncidentRepository.get_incident_by_id(incident_id)
        if not incident:
            return None

        status = StatusRepository.get_status_by_code(status_code)
        if not status:
            raise ValueError(f"Status with code '{status_code}' not found")

        incident.status = status
        incident.save()
        return incident

    @staticmethod
    def delete_incident(incident_id: int) -> bool:
        try:
            incident = Incident.objects.get(id=incident_id)
            incident.delete()
            return True
        except Incident.DoesNotExist:
            return False

    @staticmethod
    def get_incidents_with_filters(
        status_code: Optional[str] = None, source_code: Optional[str] = None
    ) -> QuerySet[Incident]:
        queryset = Incident.objects.select_related("status", "source")

        if status_code:
            queryset = queryset.filter(status__code=status_code)

        if source_code:
            queryset = queryset.filter(source__code=source_code)

        return queryset
