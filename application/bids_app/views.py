from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from .models import Bid
from .serializers import BidSerializer
from ..custom_permissions import IsResponsibleOrAuthor
from ..tender_app.models import Tender


class BidListView(ListAPIView):
    queryset = Bid.objects.filter(status=Bid.Status.PUBLISHED)
    serializer_class = BidSerializer


class BidListMyView(ListAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)


class BidCreateView(CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsResponsibleOrAuthor]


class BidUpdateView(UpdateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsResponsibleOrAuthor]

    def perform_action(self, bid, action):
        if action == 'publish':
            bid.status = Bid.Status.PUBLISHED

        elif action == 'close':
            bid.status = Bid.Status.CLOSED

        elif action == 'accept':
            bid.approval_status = Bid.ApprovalStatus.ACCEPTED
            bid.tender.status = Tender.Status.CLOSED
            bid.tender.save()

        elif action == 'reject':
            bid.approval_status = Bid.ApprovalStatus.REJECTED

        bid.save()

    def update(self, request, *args, **kwargs):
        bid = self.get_object()
        action = self.request.data.get('action')

        if action in ['publish', 'close', 'accept', 'reject']:
            self.perform_action(bid, action)
        else:
            bid.version += 1

        return Response(self.get_serializer(bid).data)


class BidRollbackView(UpdateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
