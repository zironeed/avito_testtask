from django.urls import path
from .apps import BidsAppConfig
from .views import BidRollbackView, BidListView, BidListMyView, BidCreateView, BidUpdateView, BidApprovalView


app_name = BidsAppConfig.name


urlpatterns = [
    path('<int:tender_pk>/list/', BidListView.as_view(), name='bid_list'),
    path('my/', BidListMyView.as_view(), name='bid_list_my'),
    path('new/', BidCreateView.as_view(), name='bid_create'),
    path('<int:pk>/edit/', BidUpdateView.as_view(), name='bid_update'),
    path('<int:pk>/approval/', BidApprovalView.as_view(), name='bid_update'),
    path('<int:pk>/rollback/<int:version_id>/', BidRollbackView.as_view(), name='bid_rollback'),
]