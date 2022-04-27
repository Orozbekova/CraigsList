from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from applications.account.serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer


class RegisterAPIView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = 'Вы успешно зарегистрированы. Вам отправлено письмо с активацией'
            return Response(message,status=201)
        return Response(status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()

class ActivationView(APIView):
    def get(self,request,activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activate_code = ''
            user.save()
            return Response('Вы успешно активировали свой аккаунт',status=HTTP_200_OK)
        except User.DoesNotExist:
            return Response('Активированный код не действителен',status=HTTP_400_BAD_REQUEST)

class LoginApiView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            user = request.user
            Token.objects.filter(user=user).delete()
            return Response('Вы успешно разлогинились')
        except:
            return  Response(status=status.HTTP_403_FORBIDDEN)