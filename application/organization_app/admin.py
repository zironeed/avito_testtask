from django.contrib import admin
from .models import Organization, OrganizationResponsible


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')

@admin.register(OrganizationResponsible)
class OrganizationResponsibleAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'user')
