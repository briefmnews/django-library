from django.contrib import admin

from .models import Library


class LibraryAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    list_display = ("name", "connector", "user", "sso_id", "ends_at")
    list_filter = ("connector",)
    list_select_related = ("user",)
    ordering = ("name",)
    search_fields = ("name", "user__email", "sso_id", "connector")


admin.site.register(Library, LibraryAdmin)
