from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from application.custom_permissions import IsResponsible
from .models import Tender
from .serializers import TenderSerializer


class TenderListView(ListAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer


class TenderListMyView(ListAPIView):
    serializer_class = TenderSerializer

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)


class TenderCreateView(CreateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [IsResponsible]


class TenderUpdateView(UpdateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [IsResponsible]

class TenderRollbackView(UpdateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [IsResponsible]
