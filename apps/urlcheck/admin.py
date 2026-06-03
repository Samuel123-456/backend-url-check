from django.contrib import admin

from .models import UrlAnalysisRecord


@admin.register(UrlAnalysisRecord)
class UrlAnalysisRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "created_at", "updated_at")
    search_fields = ("url",)
    readonly_fields = ("created_at", "updated_at")
