from django.db import models


class Bid(models.Model):

    class Status(models.TextChoices):
        submitted = 'Submitted'
        accepted = 'Accepted'
        rejected = 'Rejected'

    name = models.CharField(max_length=100, verbose_name='Название предложения')
    description = models.TextField(verbose_name='Описание предложения')
    status = models.CharField(choices=Status.choices, max_length=30, default=Status.submitted, verbose_name='Статус')

    tenderId = models.ForeignKey('application.tender_app.Tender', on_delete=models.CASCADE, verbose_name='Тендер')
    organizationId = models.ForeignKey('application.organization_app.Organization', on_delete=models.CASCADE,
                                       verbose_name='Организация', null=True, blank=True)
    creator = models.ForeignKey('application.user_app.Employee', on_delete=models.CASCADE, verbose_name='Создатель')

    def __str__(self):
        return self.name
