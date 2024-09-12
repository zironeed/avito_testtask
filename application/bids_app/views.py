from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from .models import Bid
from .serializers import BidSerializer


class BidListView(ListAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer


class BidListMyView(ListAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)


class BidCreateView(CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer


class BidUpdateView(UpdateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer


class BidRollbackView(UpdateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
