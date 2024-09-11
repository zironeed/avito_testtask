from django.db import models


class Tender(models.Model):

    class ServiceType(models.TextChoices):
        SERVICE = 'Service'
        PRODUCT = 'Product'
        CONSTRUCTION = 'Construction'

    name = models.CharField(max_length=100, verbose_name='Название тендера')
    description = models.TextField(verbose_name='Описание тендера')
    serviceType = models.CharField(choices=ServiceType.choices, max_length=30,
                                   default=ServiceType.SERVICE, verbose_name='Тип услуги')

    creator = models.ForeignKey('application.user_app.Employee', on_delete=models.CASCADE,
                                related_name='tenders', verbose_name='Создатель тендера')
    organization = models.ForeignKey('application.organization_app.Organization', on_delete=models.CASCADE,
                                     related_name='tenders', verbose_name='Организация')

    def __str__(self):
        return self.name



class TenderVersion(models.Model):
    pass
