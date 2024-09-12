from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from application.custom_permissions import IsResponsible
from .models import Tender
from .serializers import TenderSerializer


class TenderListView(ListAPIView):
    queryset = Tender.objects.filter(status=Tender.Status.PUBLISHED)
    serializer_class = TenderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        service = self.request.query_params.get('serviceType')
        if service:
            return queryset.filter(serviceType__iexact=service)


class TenderListMyView(ListAPIView):
    serializer_class = TenderSerializer

    def get_queryset(self):
        service = self.request.query_params.get('serviceType')
        if service:
            return self.queryset.filter(organization=self.request.user.organization, serviceType__iexact=service)
        return self.queryset.filter(organization=self.request.user.organization)


class TenderCreateView(CreateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [IsResponsible]


class TenderUpdateView(UpdateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [IsResponsible]

    def perform_action(self, tender, action):
        if action == 'publish':
            tender.status = Tender.Status.PUBLISHED
        elif action == 'close':
            tender.status = Tender.Status.CLOSED
        tender.save()

    def update(self, request, *args, **kwargs):
        tender = self.get_object()
        action = request.data.get('action')

        if action in ['publish', 'close']:
            self.perform_action(tender, action)
        elif action == 'edit':
            serializer = self.get_serializer(tender, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            tender.version += 1
            serializer.save()

        return Response(self.get_serializer(tender).data)


class TenderRollbackView(UpdateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [IsResponsible]
