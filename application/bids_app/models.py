from django.db import models


class Bid(models.Model):
    class LifeStatus(models.TextChoices):
        CREATED = 'CREATED'
        PUBLISHED = 'PUBLISHED'
        CLOSED = 'CLOSED'

    class ApprovalStatus(models.TextChoices):
        SUBMITTED = 'Submitted'
        ACCEPTED = 'Accepted'
        REJECTED = 'Rejected'

    name = models.CharField(max_length=100, verbose_name='Название предложения')
    description = models.TextField(verbose_name='Описание предложения')
    status = models.CharField(choices=LifeStatus.choices, max_length=30,
                              default=LifeStatus.CREATED, verbose_name='Статус предложения')
    approval_status = models.CharField(choices=ApprovalStatus.choices, max_length=30,
                                       default=ApprovalStatus.SUBMITTED, verbose_name='Статус согласования')
    version = models.PositiveIntegerField(default=1, verbose_name='Версия')

    tender = models.ForeignKey('application.tender_app.Tender', on_delete=models.CASCADE, verbose_name='Тендер')
    organization = models.OneToOneField('application.organization_app.Organization', on_delete=models.CASCADE,
                                        verbose_name='Организация', null=True, blank=True)
    creator = models.ForeignKey('application.user_app.Employee', on_delete=models.CASCADE, verbose_name='Создатель')

    def __str__(self):
        return self.name
