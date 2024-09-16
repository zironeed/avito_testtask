from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'pk', 'first_name', 'last_name', 'created_at', 'updated_at')
