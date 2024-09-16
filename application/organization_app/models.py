import uuid
from django.db import models
from django.utils import timezone


class Organization(models.Model):

    class OrganizationType(models.TextChoices):
        IE = 'IE'
        LLC = 'LLC'
        JSC = 'JSC'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Название организации')
    description = models.TextField(blank=True, null=True, verbose_name='Описание организации')
    type = models.CharField(max_length=3, choices=OrganizationType.choices, verbose_name='Тип организации')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'{self.name}'


class OrganizationResponsible(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    user = models.ForeignKey('user_app.Employee', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.user} - {self.organization}'
