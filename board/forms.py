from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    username = forms.CharField(
        label="Логин",
        help_text="До 150 символов. Буквы и цифры без пробелов."
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text=(
            "Минимум 8 символов.<br>"
            "Не используйте простые пароли.<br>"
            "Пароль не должен совпадать с логином."
        )
    )

    password2 = forms.CharField(
        label="Повтор пароля",
        widget=forms.PasswordInput,
        help_text="Введите тот же пароль ещё раз."
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
