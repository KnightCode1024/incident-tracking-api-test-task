from rest_framework import serializers
from api.models import Incident, Status, Source


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "code", "name", "description", "order", "is_active",]


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["id", "code", "name", "description", "is_active",]


class IncidentListSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True)
    source_name = serializers.CharField(source='source.name', read_only=True)

    class Meta:
        model = Incident
        fields = [
            "id",
            "description",
            "status",
            "status_name",
            "source",
            "source_name",
            "created_at",
            "updated_at",
        ]


class IncidentCreateSerializer(serializers.ModelSerializer):
    source_code = serializers.CharField(write_only=True)

    class Meta:
        model = Incident
        fields = ["description", "source_code"]

    def create(self, validated_data):
        from api.services import IncidentService
        
        source_code = validated_data.pop('source_code')
        description = validated_data['description']
        
        return IncidentService.create_incident(description, source_code)


class IncidentStatusUpdateSerializer(serializers.Serializer):
    status_code = serializers.CharField()

    def validate_status_code(self, value):
        from api.repositories import StatusRepository
        
        status = StatusRepository.get_status_by_code(value)
        if not status:
            raise serializers.ValidationError("Статус с указанным кодом не найден")
        return value