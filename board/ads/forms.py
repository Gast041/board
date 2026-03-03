# board/ads/forms.py
# =========================
# FORMS ДЛЯ ОБЪЯВЛЕНИЙ
# =========================

from django import forms
from .models import Ad, Category


class AdForm(forms.ModelForm):
    # =========================
    # ПОЛЕ КАТЕГОРИИ
    # =========================
    # Показываем только ПОДРУБРИКИ (у которых parent != NULL)
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True, parent__isnull=False).select_related("parent"),
        required=False,
        empty_label="— Выбери подрубрику —",
        label="Рубрика",
    )

    class Meta:
        model = Ad
        fields = ["title", "description", "price", "category"]

        labels = {
            "title": "Заголовок",
            "description": "Описание",
            "price": "Цена",
        }