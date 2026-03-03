# board/ads/admin.py
# =========================
# АДМИНКА (управление рубриками и объявлениями)
# =========================

from django.contrib import admin
from .models import Ad, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "sort_order", "is_active")
    list_filter = ("is_active", "parent")
    search_fields = ("name", "slug")
    ordering = ("parent__id", "sort_order", "name")
    prepopulated_fields = {"slug": ("name",)}  # удобно, но можешь убрать


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description", "author__username")
    ordering = ("-id",)