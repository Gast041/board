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

    # Название (что видит пользователь)
    name = models.CharField(max_length=80)

    # ЧПУ/ссылка-ключ (для будущих красивых URL: /c/nedvizhimost/kvartiry/)
    # unique=True — чтобы не было дублей
    slug = models.SlugField(max_length=120, unique=True)

    # Родитель: если NULL -> это рубрика, если не NULL -> подрубрика
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,       # если удалят рубрику — удалятся её подрубрики
        null=True,
        blank=True,
        related_name="children"
    )

    # Порядок вывода (для главной страницы и меню)
    sort_order = models.PositiveIntegerField(default=0)

    # Можно выключать рубрики без удаления
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
        # Для админки: "Недвижимость / Квартиры"
        if self.parent:
            return f"{self.parent.name} / {self.name}"
        return self.name

    @property
    def is_root(self) -> bool:
        """True если это рубрика верхнего уровня (без родителя)"""
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

    # Автор объявления (правильно: через AUTH_USER_MODEL)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ads"
    )

    # Категория (мы сохраняем именно подрубрику; можно оставлять пустой)
    # PROTECT — нельзя удалить категорию, если на неё уже есть объявления
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ads"
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