from django.contrib import admin
from .models import Bid


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'status', 'approval_status', 'tender', 'organization', 'creator')
