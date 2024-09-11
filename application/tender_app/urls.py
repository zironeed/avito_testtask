from django.urls import path
from .apps import TenderAppConfig
from .views import TenderListView, TenderListMyView, TenderCreateView, TenderUpdateView, TenderRollbackView


app_name = TenderAppConfig.name


urlpatterns = [
    path('', TenderListView.as_view(), name='tender_list'),
    path('my/', TenderListMyView.as_view(), name='tender_list_my'),
    path('new/', TenderCreateView.as_view(), name='tender_create'),
    path('<int:pk>/edit/', TenderUpdateView.as_view(), name='tender_update'),
    path('<int:pk>/rollback/<int:version_id>/', TenderRollbackView.as_view(), name='tender_rollback'),
]