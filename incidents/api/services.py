from typing import List, Optional

from django.http import Http404
from django.core.exceptions import ValidationError

from api.models import Incident
from api.repositories import IncidentRepository, StatusRepository, SourceRepository


class IncidentService:
    @staticmethod
    def create_incident(
        description: str, source_code: str, status_code: str = None
    ) -> Incident:
        if not description or not description.strip():
            raise ValidationError("Описание инцидента не может быть пустым")

        if not source_code:
            raise ValidationError("Код источника обязателен")

        return IncidentRepository.create_incident(description, source_code, status_code)

    @staticmethod
    def get_incidents(
        status_code: Optional[str] = None, source_code: Optional[str] = None
    ) -> List[Incident]:
        return list(
            IncidentRepository.get_incidents_with_filters(status_code, source_code)
        )

    @staticmethod
    def get_incident_detail(incident_id: int) -> Incident:
        incident = IncidentRepository.get_incident_by_id(incident_id)
        if not incident:
            raise Http404(f"Инцидент с ID {incident_id} не найден")
        return incident

    @staticmethod
    def update_incident_status(incident_id: int, status_code: str) -> Incident:
        if not status_code:
            raise ValidationError("Код статуса обязателен")

        incident = IncidentRepository.update_incident_status(incident_id, status_code)
        if not incident:
            raise Http404(f"Инцидент с ID {incident_id} не найден")
        return incident

    @staticmethod
    def get_metadata():
        return {
            "statuses": StatusRepository.get_available_statuses(),
            "sources": SourceRepository.get_available_sources(),
        }

    @staticmethod
    def initialize_default_data():
        StatusRepository.create_default_statuses()
        SourceRepository.create_default_sources()
