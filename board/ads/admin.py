# board/ads/admin.py
# =========================
# АДМИНКА (управление рубриками и объявлениями)
# =========================

from django.contrib import admin
from django.utils import timezone

from .models import Ad, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Что видно в списке рубрик
    list_display = ("id", "name", "parent", "sort_order", "is_active")

    # Фильтры справа
    list_filter = ("is_active", "parent")

    # Поиск сверху
    search_fields = ("name", "slug")

    # Сортировка
    ordering = ("parent__id", "sort_order", "name")

    # Автозаполнение slug
    prepopulated_fields = {"slug": ("name",)}


@admin.action(description="Перевести выбранные объявления в архив")
def make_archived(modeladmin, request, queryset):
    queryset.update(status=Ad.STATUS_ARCHIVED)


@admin.action(description="Вернуть выбранные объявления в активные на 30 дней")
def make_active_for_30_days(modeladmin, request, queryset):
    now = timezone.now()
    queryset.update(
        status=Ad.STATUS_ACTIVE,
        published_at=now,
        expires_at=now + timezone.timedelta(days=30),
    )


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    # Что видно в списке объявлений
    list_display = (
        "id",
        "title",
        "author",
        "category",
        "status",
        "city",
        "phone",
        "published_at",
        "expires_at",
        "is_expired_admin",
    )

    # Фильтры справа
    list_filter = (
        "status",
        "category",
        "city",
        "published_at",
        "expires_at",
        "created_at",
    )

    # Поиск сверху
    search_fields = (
        "title",
        "description",
        "author__username",
        "phone",
        "city",
        "address",
    )

    # Сортировка
    ordering = ("-published_at", "-id")

    # Только для чтения в форме админки
    readonly_fields = (
        "created_at",
        "published_at",
        "expires_at",
        "image_preview",
    )

    # Поля в форме редактирования
    fieldsets = (
        ("Основное", {
            "fields": (
                "title",
                "description",
                "price",
                "author",
                "category",
            )
        }),
        ("Контакты и адрес", {
            "fields": (
                "phone",
                "city",
                "address",
            )
        }),
        ("Фото", {
            "fields": (
                "image",
                "image_preview",
            )
        }),
        ("Статус и сроки", {
            "fields": (
                "status",
                "published_at",
                "expires_at",
                "created_at",
            )
        }),
    )

    # Массовые действия
    actions = (make_archived, make_active_for_30_days)

    def is_expired_admin(self, obj):
        return obj.is_expired
    is_expired_admin.short_description = "Срок истёк"
    is_expired_admin.boolean = True

    def image_preview(self, obj):
        if obj.image:
            return admin.helpers.format_html(
                '<img src="{}" style="max-width:220px; border-radius:10px;" />',
                obj.image.url
            )
        return "Нет фото"
    image_preview.short_description = "Превью"