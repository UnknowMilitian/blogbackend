from django.contrib import admin
from .models import CustomUser, BlogCategory, Blog
from django.utils.text import slugify


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "description"]


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.title)
        obj.save()


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "views"]
    date_hierarchy = "date"  # Иерархия даты для навигации
    list_per_page = 10

    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.title)
        obj.save()
