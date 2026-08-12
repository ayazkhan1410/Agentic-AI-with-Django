from django.contrib import admin

from agents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "owner", "active",
        "created_at", "updated_at"
    )
    list_filter = ("active", "created_at")
    search_fields = ("title", "content", "owner__username")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("active",)
    ordering = ("-created_at",)
