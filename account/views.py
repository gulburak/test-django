from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (RegistrationSerializer, ActivationSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, LoginSerializer, ForgotPassCompleteSerializer)
class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response('akkaunt uspeshno sozdan', status=201)

class ActivationView(APIView):
    def post(self, request):
        data = request.data
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response('akkaunt uspeshno aktivirovan', status = status.HTTP_200_OK)

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        Token.objects.filter(user = user).delete()
        return Response('vi uspeshno zaregistrirovalis')

class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('parol uspeshno obnovlen')

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('vam vislano soobchenie dlya vostanovleniya')

class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPassCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_new_passord()
            return Response('parol usepeshno obnovlen')


class ForgotPasswordCompleteView(APIView):