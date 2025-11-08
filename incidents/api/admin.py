from django.contrib import admin
from api.models import Incident, Status, Source


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_editable = ['is_active']


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ['id', 'description_short', 'status', 'source', 'created_at']
    list_filter = ['status', 'source', 'created_at']
    search_fields = ['description']
    readonly_fields = ['created_at', 'updated_at']
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Описание'