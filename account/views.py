from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (RegistrationSerializer, ActivationSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, LoginSerializer)
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

class LogoutView():
    pass
class ChangePasswordView():
    pass
class ForgotPasswordView():
    pass


