from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import Http404

from api.services import IncidentService
from api.serializers import (
    IncidentListSerializer,
    IncidentCreateSerializer,
    IncidentStatusUpdateSerializer,
)


class IncidentViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        status_filter = request.query_params.get("status")
        source_filter = request.query_params.get("source")

        try:
            incidents = IncidentService.get_incidents(
                status_code=status_filter, source_code=source_filter
            )
            serializer = IncidentListSerializer(incidents, many=True)
            return Response({"count": len(incidents), "results": serializer.data})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request: Request) -> Response:
        serializer = IncidentCreateSerializer(data=request.data)

        if serializer.is_valid():
            try:
                incident = IncidentService.create_incident(
                    description=serializer.validated_data["description"],
                    source_code=serializer.validated_data["source_code"],
                )
                response_serializer = IncidentListSerializer(incident)
                return Response(
                    response_serializer.data, status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request: Request, pk: int = None) -> Response:
        try:
            incident = IncidentService.get_incident_detail(pk)
            serializer = IncidentListSerializer(incident)
            return Response(serializer.data)
        except Http404:
            return Response(
                {"error": "Инцидент не найден"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["patch", "put"])
    def status(self, request: Request, pk: int = None) -> Response:
        serializer = IncidentStatusUpdateSerializer(data=request.data)

        if serializer.is_valid():
            try:
                incident = IncidentService.update_incident_status(
                    pk, serializer.validated_data["status_code"]
                )
                response_serializer = IncidentListSerializer(incident)
                return Response(response_serializer.data)
            except Http404:
                return Response(
                    {"error": "Инцидент не найден"}, status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def metadata(self, request: Request) -> Response:
        metadata = IncidentService.get_metadata()
        return Response(metadata)
