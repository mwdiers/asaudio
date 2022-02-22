from django.contrib import admin
from .models import Developer, Category, Software


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ["name", "url"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class SoftwareAdmin(admin.ModelAdmin):
    list_display = ["name", "developer", "category"]


admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Software, SoftwareAdmin)
