from django.contrib import admin
from .models import Developer, Category, Software


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ("name", "url",)
    readonly_fields = ("id",)
    search_fields = ("name",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sequence")


class SoftwareAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "developer", "category", "url", "free", "active")
    list_editable = ("category", "version", "url", "free", "active")
    list_filter = ("category", "active")
    search_fields = ("name", "developer__name", "free")
    save_as = True
    save_as_continue = False


admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Software, SoftwareAdmin)