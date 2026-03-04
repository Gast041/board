# =========================
# board/ads/forms.py
# Формы приложения "ads"
# =========================

from django import forms
from .models import Ad, Category


# =========================
# ФОРМА: СОЗДАНИЕ/РЕДАКТИРОВАНИЕ ОБЪЯВЛЕНИЯ
# =========================
class AdForm(forms.ModelForm):
    """
    Форма объявления.

    ВАЖНО:
    - category выбираем только из "подрубрик" (parent != None)
    - в select показываем группами (optgroup): Рубрика -> подрубрики
    - стилизуем поля через widgets (чтобы HTML был чистый)
    """

    class Meta:
        model = Ad
        fields = ["title", "category", "description", "price"]

        widgets = {
            # -------------------------
            # Заголовок
            # -------------------------
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Например: Продам iPhone 13",
            }),

            # -------------------------
            # Рубрика / Подрубрика (select)
            # -------------------------
            "category": forms.Select(attrs={
                "class": "form-input",
            }),

            # -------------------------
            # Описание
            # -------------------------
            "description": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Опиши состояние, комплект, район, телефон и т.д.",
                "rows": 6,
            }),

            # -------------------------
            # Цена
            # -------------------------
            "price": forms.NumberInput(attrs={
                "class": "form-input",
                "placeholder": "Цена (не обязательно)",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # =========================
        # 1) Берём ТОЛЬКО подрубрики (parent != NULL)
        # 2) Группируем их по родительской рубрике в optgroup
        #    Получаем: "Недвижимость" -> [Квартиры, Комнаты...]
        # =========================
        subcats = (
            Category.objects.filter(is_active=True, parent__isnull=False)
            .select_related("parent")
            .order_by("parent__sort_order", "parent__name", "sort_order", "name")
        )

        grouped = {}
        for c in subcats:
            parent_name = c.parent.name if c.parent else "Без рубрики"
            grouped.setdefault(parent_name, []).append((c.id, c.name))

        # choices формата:
        # [("", "---------"), ("Недвижимость", [(id, "Квартиры"), ...]), ...]
        self.fields["category"].choices = [("", "---------")] + [
            (group, items) for group, items in grouped.items()
        ]

        # =========================
        # Подписи полей (как ты любишь — понятно)
        # =========================
        self.fields["title"].label = "Заголовок"
        self.fields["category"].label = "Рубрика"
        self.fields["description"].label = "Описание"
        self.fields["price"].label = "Цена"