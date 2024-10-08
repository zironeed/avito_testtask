from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from .models import Bid
from .serializers import BidSerializer
from ..custom_permissions import IsResponsibleOrAuthor, IsTenderResponsible
from ..tender_app.models import Tender


class BidListView(ListAPIView):
    """
    Список всех предложений с флагом PUBLISHED для одного тендера
    """

    serializer_class = BidSerializer

    def get_queryset(self):
        tender_pk = self.kwargs.get('tender_pk')
        return Bid.objects.filter(status=Bid.LifeStatus.PUBLISHED, tender__pk=tender_pk)


class BidListMyView(ListAPIView):
    """
    Список предложений пользователя/организации
    """

    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)


class BidCreateView(CreateAPIView):
    """
    Создание предложений
    """

    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsResponsibleOrAuthor]


class BidUpdateView(UpdateAPIView):
    """
    Обновление предложений. Метод PUT закрыт, PATCH - открыт
    Можно изменить информацию о предложении (название, описание и прочее), либо изменить его флаги
    Для смены флага используйте "action", например:
    {"action": "publish"}
    Доступные actions:
    * publish - публикация
    * close - закрытие
    """

    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsResponsibleOrAuthor]

    def perform_action(self, bid, action):
        if action == 'publish':
            bid.status = Bid.LifeStatus.PUBLISHED

        elif action == 'close':
            bid.status = Bid.LifeStatus.CLOSED

        bid.save()

    def update(self, request, *args, **kwargs):
        bid = self.get_object()
        action = self.request.data.get('action')

        if action in ['publish', 'close']:
            self.perform_action(bid, action)
        else:
            serializer = self.get_serializer(bid, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            bid.version += 1
            serializer.save()

        return Response(self.get_serializer(bid).data)

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Method PUT is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BidApprovalView(UpdateAPIView):
    """
    Обновление статуса одобрения предложений. Метод PUT закрыт, PATCH - открыт
    Доступно только для владельцев тендера (ответственных за организацию)
    Для смены флага используйте "action", например:
    {"action": "accept"}
    Доступные actions:
    * accept - подтверждение
    * reject - отклонение
    """

    serializer_class = BidSerializer
    queryset = Bid.objects.all()
    permission_classes = [IsTenderResponsible]

    def perform_action(self, bid, action):
        if action == 'accept':
            bid.approval_status = Bid.ApprovalStatus.ACCEPTED
            bid.tender.status = Tender.Status.CLOSED
            bid.tender.save()

        elif action == 'reject':
            bid.approval_status = Bid.ApprovalStatus.REJECTED

        bid.save()

    def update(self, request, *args, **kwargs):
        bid = self.get_object()
        action = self.request.data.get('action')

        if action in ['accept', 'reject']:
            self.perform_action(bid, action)

        return Response(self.get_serializer(bid).data)

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Method PUT is not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
