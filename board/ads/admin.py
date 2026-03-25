# board/ads/admin.py
# =========================
# АДМИНКА (управление рубриками и объявлениями)
# =========================

from datetime import timedelta

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import Ad, Category


# =========================
# ФИЛЬТР: срок истёк / не истёк
# =========================
class ExpiredFilter(admin.SimpleListFilter):
    title = "Срок публикации"
    parameter_name = "expired"

    def lookups(self, request, model_admin):
        return (
            ("no", "Активен по сроку"),
            ("yes", "Срок истёк"),
        )

    def queryset(self, request, queryset):
        now = timezone.now()

        if self.value() == "yes":
            return queryset.filter(expires_at__lte=now)

        if self.value() == "no":
            return queryset.filter(expires_at__gt=now)

        return queryset


# =========================
# ФИЛЬТР: снято пользователем / нет
# =========================
class HiddenByUserFilter(admin.SimpleListFilter):
    title = "Снято пользователем"
    parameter_name = "hidden_by_user"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Да"),
            ("no", "Нет"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(deleted_by_user_at__isnull=False)

        if self.value() == "no":
            return queryset.filter(deleted_by_user_at__isnull=True)

        return queryset


@admin.action(description="Одобрить выбранные объявления")
def approve_ads(modeladmin, request, queryset):
    now = timezone.now()
    queryset.update(
        status=Ad.STATUS_ACTIVE,
        moderation_note="",
        reviewed_at=now,
        reviewed_by=request.user,
        published_at=now,
        expires_at=now + timedelta(days=30),
        deleted_by_user_at=None,
    )


@admin.action(description="Отклонить выбранные объявления")
def reject_ads(modeladmin, request, queryset):
    now = timezone.now()
    queryset.update(
        status=Ad.STATUS_REJECTED,
        reviewed_at=now,
        reviewed_by=request.user,
        deleted_by_user_at=None,
    )


@admin.action(description="Перевести выбранные объявления в архив")
def make_archived(modeladmin, request, queryset):
    now = timezone.now()
    queryset.update(
        status=Ad.STATUS_ARCHIVED,
        reviewed_at=now,
        reviewed_by=request.user,
    )


@admin.action(description="Вернуть выбранные объявления на модерацию")
def send_to_pending(modeladmin, request, queryset):
    queryset.update(
        status=Ad.STATUS_PENDING,
        moderation_note="",
        reviewed_at=None,
        reviewed_by=None,
        deleted_by_user_at=None,
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "sort_order", "is_active")
    list_filter = ("is_active", "parent")
    search_fields = ("name", "slug")
    ordering = ("parent__id", "sort_order", "name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
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
        "deleted_by_user_at",
        "reviewed_at",
        "reviewed_by",
        "is_expired_admin",
    )

    list_filter = (
        "status",
        "category",
        "city",
        "published_at",
        "expires_at",
        ExpiredFilter,
        HiddenByUserFilter,
        "reviewed_at",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "author__username",
        "phone",
        "city",
        "address",
        "moderation_note",
    )

    ordering = ("-created_at", "-id")

    readonly_fields = (
        "created_at",
        "published_at",
        "expires_at",
        "deleted_by_user_at",
        "reviewed_at",
        "reviewed_by",
        "image_preview",
    )

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
        ("Модерация", {
            "fields": (
                "status",
                "moderation_note",
                "reviewed_at",
                "reviewed_by",
            )
        }),
        ("Сроки и история", {
            "fields": (
                "published_at",
                "expires_at",
                "deleted_by_user_at",
                "created_at",
            )
        }),
    )

    actions = (
        approve_ads,
        reject_ads,
        make_archived,
        send_to_pending,
    )

    def save_model(self, request, obj, form, change):
        now = timezone.now()

        if change:
            old_obj = Ad.objects.get(pk=obj.pk)
            status_changed = old_obj.status != obj.status
            note_changed = old_obj.moderation_note != obj.moderation_note
        else:
            status_changed = True
            note_changed = bool(obj.moderation_note)

        if status_changed or note_changed:
            obj.reviewed_at = now
            obj.reviewed_by = request.user

        if status_changed and obj.status == Ad.STATUS_ACTIVE:
            obj.published_at = now
            obj.expires_at = now + timedelta(days=30)
            obj.deleted_by_user_at = None
            obj.moderation_note = ""

        if obj.status in (Ad.STATUS_PENDING, Ad.STATUS_REJECTED):
            obj.deleted_by_user_at = None

        super().save_model(request, obj, form, change)

    def is_expired_admin(self, obj):
        return obj.is_expired
    is_expired_admin.short_description = "Срок истёк"
    is_expired_admin.boolean = True

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:220px; border-radius:10px; border:1px solid #eee;" />',
                obj.image.url
            )
        return "Нет фото"
    image_preview.short_description = "Превью"
