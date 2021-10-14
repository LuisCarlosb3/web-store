import re

from django.contrib.auth import authenticate, login
from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.serializers import LoginSerializer, UserSerializer
from accounts.usecases import user_login


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class  = UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        else:
            return super().get_permissions()

    @transaction.atomic
    def register(self, request):
        data_serialized = UserSerializer(data=request.data)
        data_serialized.is_valid(raise_exception=True)
        data_serialized.save()
        return Response(data_serialized.data)

    @action(detail=False, methods=['post'])
    def login(self, request, pk=None):
        user_data = LoginSerializer(data=request.data)
        user_data.is_valid(raise_exception=True)
        payload = user_data.data
        user = user_login(email=payload["email"], password=payload["password"])
        if user and user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            login(request=request, user=user)
            content = {
                'token': token.key
            }
            return Response(data=content, status=HTTP_200_OK)
        else:
            content = {
                "message": "E-mail ou senha não conferem"
            }
            return Response(data=content, status=HTTP_403_FORBIDDEN)

    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
