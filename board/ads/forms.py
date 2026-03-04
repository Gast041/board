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
    - стилизуем поля через widgets (чтобы HTML был чистый)
    """

    class Meta:
        model = Ad
        fields = ["title", "category", "description", "price"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Например: Продам iPhone 13",
            }),
            "category": forms.Select(attrs={
                "class": "form-input",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Опиши состояние, комплект, район, телефон и т.д.",
                "rows": 6,
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-input",
                "placeholder": "Цена (не обязательно)",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Показываем только ПОДРУБРИКИ, чтобы объявление было именно в конечной категории
        self.fields["category"].queryset = (
            Category.objects.filter(is_active=True, parent__isnull=False)
            .select_related("parent")
            .order_by("parent__sort_order", "parent__name", "sort_order", "name")
        )

        # Красивые подписи (Родитель → Подрубрика)
        self.fields["category"].label_from_instance = lambda obj: f"{obj.parent.name} → {obj.name}"

        # Чуть более дружелюбные подписи
        self.fields["title"].label = "Заголовок"
        self.fields["category"].label = "Рубрика"
        self.fields["description"].label = "Описание"
        self.fields["price"].label = "Цена"