from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from application.custom_permissions import IsResponsible
from .models import Tender
from .serializers import TenderSerializer
from ..organization_app.models import OrganizationResponsible


class TenderListView(ListAPIView):
    queryset = Tender.objects.filter(status=Tender.Status.PUBLISHED)
    serializer_class = TenderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        service = self.request.query_params.get('serviceType')
        if service:
            return queryset.filter(serviceType__iexact=service)
        return queryset


class TenderListMyView(ListAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [IsResponsible]

    def get_queryset(self):
        responsible = OrganizationResponsible.objects.filter(user=self.request.user).first()
        service = self.request.query_params.get('serviceType')
        if service:
            return self.queryset.filter(organization=responsible.organization.id, serviceType__iexact=service)
        return self.queryset.filter(organization=responsible.organization.id)


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
        else:
            serializer = self.get_serializer(tender, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            tender.version += 1
            serializer.save()

        return Response(self.get_serializer(tender).data)

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Method PUT is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
