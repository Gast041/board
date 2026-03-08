# board/ads/models.py
# =========================
# МОДЕЛИ ПРИЛОЖЕНИЯ ADS
# (объявления + рубрики)
# =========================

from django.conf import settings
from django.db import models


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

    # Главное фото объявления
    image = models.ImageField(
        upload_to="listing_photos/",
        null=True,
        blank=True,
        verbose_name="Фото"
    )

    # Дата создания
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.title