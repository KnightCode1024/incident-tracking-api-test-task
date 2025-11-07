from django.contrib import admin

from api.models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    pass