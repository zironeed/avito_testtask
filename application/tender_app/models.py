from django.db import models


class Tender(models.Model):

    class Status(models.TextChoices):
        CREATED = 'CREATED'
        PUBLISHED = 'PUBLISHED'
        CLOSED = 'CLOSED'

    class ServiceType(models.TextChoices):
        SERVICE = 'Service'
        PRODUCT = 'Product'
        CONSTRUCTION = 'Construction'

    name = models.CharField(max_length=100, verbose_name='Название тендера')
    description = models.TextField(verbose_name='Описание тендера')
    serviceType = models.CharField(choices=ServiceType.choices, max_length=30,
                                   default=ServiceType.SERVICE, verbose_name='Тип услуги')
    status = models.CharField(choices=Status.choices, max_length=30,
                              default=Status.CREATED, verbose_name='Статус тендера')
    version = models.PositiveIntegerField(default=1, verbose_name='Версия')

    creator = models.ForeignKey('user_app.Employee', on_delete=models.CASCADE,
                                related_name='tenders', verbose_name='Создатель тендера')
    organization = models.ForeignKey('organization_app.Organization', on_delete=models.CASCADE,
                                     related_name='tenders', verbose_name='Организация')

    def __str__(self):
        return self.name
