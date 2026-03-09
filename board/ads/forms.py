# =========================
# board/ads/forms.py
# Формы приложения "ads"
# =========================

from django import forms
from .models import Ad, Category


# =========================
# ФОРМА: СОЗДАНИЕ / РЕДАКТИРОВАНИЕ ОБЪЯВЛЕНИЯ
# =========================
class AdForm(forms.ModelForm):
    """
    Форма объявления.

    ЛОГИКА:
    1) Сначала выбираем РУБРИКУ (верхний уровень, parent=None)
    2) Потом показываем только ПОДРУБРИКИ этой рубрики
    3) Всё без JavaScript
    """

    # Рубрика
    parent_category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True, parent__isnull=True).order_by("sort_order", "name"),
        required=False,
        empty_label="— Выбери рубрику —",
        label="Рубрика",
        widget=forms.Select(attrs={
            "class": "form-input",
        }),
    )

    # Подрубрика
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        empty_label="— Сначала выбери подрубрику —",
        label="Подрубрика",
        widget=forms.Select(attrs={
            "class": "form-input",
        }),
    )

    class Meta:
        model = Ad
        fields = ["title", "category", "description", "price", "phone", "image"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Например: Продам iPhone 13",
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
            "phone": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "+7 900 123-45-67",
                "inputmode": "tel",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-input",
                "accept": "image/*",
            }),
        }

    def __init__(self, *args, **kwargs):
        parent_id = kwargs.pop("parent_id", None)
        super().__init__(*args, **kwargs)

        self.fields["title"].label = "Заголовок"
        self.fields["description"].label = "Описание"
        self.fields["price"].label = "Цена"
        self.fields["phone"].label = "Телефон"
        self.fields["image"].label = "Фото"

        if self.instance and self.instance.pk and self.instance.category:
            self.fields["parent_category"].initial = self.instance.category.parent_id
            self.fields["category"].queryset = (
                Category.objects.filter(
                    is_active=True,
                    parent_id=self.instance.category.parent_id
                ).order_by("sort_order", "name")
            )

        if "parent_category" in self.data:
            try:
                selected_parent_id = int(self.data.get("parent_category"))
                self.fields["category"].queryset = (
                    Category.objects.filter(
                        is_active=True,
                        parent_id=selected_parent_id
                    ).order_by("sort_order", "name")
                )
            except (TypeError, ValueError):
                self.fields["category"].queryset = Category.objects.none()

        elif parent_id:
            try:
                parent_id = int(parent_id)
                self.fields["parent_category"].initial = parent_id
                self.fields["category"].queryset = (
                    Category.objects.filter(
                        is_active=True,
                        parent_id=parent_id
                    ).order_by("sort_order", "name")
                )
            except (TypeError, ValueError):
                self.fields["category"].queryset = Category.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        parent_category = cleaned_data.get("parent_category")
        category = cleaned_data.get("category")

        if parent_category and not category:
            self.add_error("category", "Выбери подрубрику.")

        if parent_category and category and category.parent_id != parent_category.id:
            self.add_error("category", "Подрубрика не относится к выбранной рубрике.")

        return cleaned_data