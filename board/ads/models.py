from django.db import models
from django.contrib.auth.models import User

class Ad(models.Model):
    # Заголовок объявления
    title = models.CharField(max_length=200)

    # Описание
    description = models.TextField(blank=True)

    # Цена (можно null/blank чтобы не обязательно)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Автор объявления (пользователь)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Дата создания
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
