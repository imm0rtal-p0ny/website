from rest_framework import viewsets, views
from .permissions import ReadOnly, IsOwnerOrSuperUser, UserRegisterUpdatePermissions, UserAuthenticatedAndNotAuthorized
from .serializers import BoardSerializer, RegionSerializer, DivisionSerializer, ConditionSerializer, UserSerializer
from board.models import Board, Region, Division, Condition
from user.models import CustomUser, ConfirmationCode
from rest_framework.response import Response
from django.core.mail import send_mail
from user.user_exception import NotUserException, NotUserCodeException, TimeOutCodeException, CodeDoNotMatchException



class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (IsOwnerOrSuperUser,)

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


class UserViewSets(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserRegisterUpdatePermissions,)


class VerificationAPIView(views.APIView):
    permission_classes = (UserAuthenticatedAndNotAuthorized, )

    def get(self, request):
        try:
            new_code = ConfirmationCode.created_code(request.user.email)

            if new_code:
                send_mail(
                    'Code verification',
                    new_code,
                    'imm0rtal-p0ny@ukr.net',
                    [request.user.email],
                    fail_silently=False,
                )
                data = {'Information': f'Code send you email {request.user.email}'}
        except NotUserException as message:
            data = {'message': str(message)}

        return Response(data)

    def post(self, request):
        data = {'error': 'Request takes 1 position argument "code"'}
        if len(request.data) == 1:
            code = request.data.get('code')
            print(111)
            if not code:
                return Response(data)
            try:
                result = ConfirmationCode.check_valid_code(request.user.email, code)
                if result:
                    CustomUser.verification(request.user.email)
                    data = {"message": "Done"}
            except (NotUserException, NotUserCodeException, TimeOutCodeException, CodeDoNotMatchException) as message:
                print(2222, message)
                data = {"error": str(message)}

        return Response(data)

