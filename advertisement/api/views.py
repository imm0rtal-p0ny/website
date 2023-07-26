from rest_framework import viewsets, views, generics
from rest_framework.permissions import IsAuthenticated
from .permissions import ReadOnly, IsOwnerOrReadOnly, IsAuthorized
from .serializers import BoardSerializer, RegionSerializer, DivisionSerializer, ConditionSerializer
from board.models import Board, Region, Division, Condition


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    # permission_classes = (IsOwnerOrReadOnly, IsAuthorized)

    def get_queryset(self):
        queryset = Board.objects.filter(status__name='Public')
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('photo'):
            instance.update_photo(old_photo=request.data.get('photo'), is_api=True)
            request.data['photo'] = ''
        if request.data.get('clear_photo'):
            instance.update_photo(clear_photo=request.data.get('clear_photo'), is_api=True)

        response = super().update(request, *args, **kwargs)

        return response


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (ReadOnly,)


class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = (ReadOnly,)


class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = (ReadOnly,)
