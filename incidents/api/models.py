from django.db import models
from django.utils import timezone


class Status(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='Код',)
    name = models.CharField(max_length=50, verbose_name='Название',)
    description = models.TextField(blank=True, verbose_name='Описание',)
    order = models.IntegerField(default=0, verbose_name='Порядок',)
    is_active = models.BooleanField(default=True, verbose_name='Активен',)
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Source(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='Код',)
    name = models.CharField(max_length=50, verbose_name='Название',)
    description = models.TextField(blank=True, verbose_name='Описание',)
    is_active = models.BooleanField(default=True, verbose_name='Активен',)
    
    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Incident(models.Model):
    description = models.TextField(verbose_name='Описание')
    status = models.ForeignKey(
        Status, 
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )
    source = models.ForeignKey(
        Source, 
        on_delete=models.PROTECT,
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
        return f"Incident ID: {self.id}; Status: {self.status.name}"