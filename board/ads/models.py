# board/ads/models.py
# =========================
# МОДЕЛИ ПРИЛОЖЕНИЯ ADS
# (объявления + рубрики)
# =========================

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


def default_expires_at():
    """
    По умолчанию объявление активно 30 дней.
    """
    return timezone.now() + timedelta(days=30)


# =========================
# РУБРИКИ / ПОДРУБРИКИ
# =========================
class Category(models.Model):
    """
    Category — универсальная модель для:
    - рубрики (parent = NULL)
    - подрубрики (parent = ссылка на рубрику)

    Пример:
    Недвижимость (parent=None)
      └ Квартиры (parent=Недвижимость)
    """

    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=120, unique=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]
        indexes = [
            models.Index(fields=["parent", "sort_order"]),
            models.Index(fields=["slug"]),
        ]
        verbose_name = "Рубрика"
        verbose_name_plural = "Рубрики"

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} / {self.name}"
        return self.name

    @property
    def is_root(self) -> bool:
        return self.parent_id is None


# =========================
# ОБЪЯВЛЕНИЯ
# =========================
class Ad(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Активно"),
        (STATUS_ARCHIVED, "В архиве"),
    ]

    # Заголовок объявления
    title = models.CharField(max_length=200)

    # Описание
    description = models.TextField(blank=True)

    # Цена (не обязательно)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Автор объявления
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ads"
    )

    # Категория (сохраняем именно подрубрику)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ads"
    )

    # Населённый пункт
    city = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Населённый пункт"
    )

    # Адрес
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Адрес"
    )

    # Телефон для связи
    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Телефон"
    )

    # Главное фото объявления
    image = models.ImageField(
        upload_to="listing_photos/",
        null=True,
        blank=True,
        verbose_name="Фото"
    )

    # Статус объявления
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        db_index=True,
        verbose_name="Статус"
    )

    # Дата публикации
    published_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        verbose_name="Дата публикации"
    )

    # Дата окончания публикации
    expires_at = models.DateTimeField(
        default=default_expires_at,
        db_index=True,
        verbose_name="Активно до"
    )

    # Когда пользователь снял объявление с публикации
    deleted_by_user_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Снято пользователем"
    )

    # Дата создания записи
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at", "-id"]
        indexes = [
            models.Index(fields=["status", "expires_at"]),
            models.Index(fields=["published_at"]),
            models.Index(fields=["category"]),
            models.Index(fields=["deleted_by_user_at"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Если срок публикации не задан — ставим 30 дней от даты публикации.
        """
        if not self.published_at:
            self.published_at = timezone.now()

        if not self.expires_at:
            self.expires_at = self.published_at + timedelta(days=30)

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return self.expires_at <= timezone.now()

    @property
    def is_hidden_by_user(self):
        return self.deleted_by_user_at is not None

    @property
    def is_public_active(self):
        return (
            self.status == self.STATUS_ACTIVE
            and not self.is_expired
            and not self.is_hidden_by_user
        )

    @property
    def display_status(self):
        if self.is_hidden_by_user:
            return "Снято пользователем"
        if self.status == self.STATUS_ARCHIVED or self.is_expired:
            return "В архиве"
        return "Активно"