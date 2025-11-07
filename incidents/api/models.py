from django.db import models
from django.utils import timezone


class Incident(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Открыт'
        IN_PROGRESS = 'in_progress', 'В работе'
        RESOLVED = 'resolved', 'Решен'
        CLOSED = 'closed', 'Закрыт'

    class Source(models.TextChoices):
        OPERATOR = 'operator', 'Оператор'
        MONITORING = 'monitoring', 'Мониторинг'
        PARTNER = 'partner', 'Партнер'

    description = models.TextField(
        verbose_name='Описание'
        )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name='Статус'
    )
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        verbose_name='Источник'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Время создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления'
    )

    class Meta:
        verbose_name = 'Инцидент'
        verbose_name_plural = 'Инциденты'
        ordering = ['-created_at']

    def __str__(self):
        return f"Incident ID: {self.id}; Status: {self.status}"