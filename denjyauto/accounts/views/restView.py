#view for clients-user

from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from denjyauto.accounts.serializers import LoginRequestSerializer, LoginResponseSerializer, LogoutRequestSerializer, \
    LogoutResponseSerializer, ClientChangePasswordSerializer


@extend_schema(
    tags=['auth'],
    summary='Login endpoint',
    description='Authenticate client-user and back response',
    request=LoginRequestSerializer,
    responses={
        200:LoginResponseSerializer,
        401: "Invalid Username or Password",
    }
)
class LoginClientsUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Login successful",
            },
            status=status.HTTP_200_OK
        )

@extend_schema(
    tags=['auth'],
    summary='Logout endpoint',
    description='Blacklist refresh token',
    request=LogoutRequestSerializer,
    responses={
        200:LogoutResponseSerializer,
        400: "Invalid or expired token",
    }
)
class LogoutClientsUserView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': "Logout successful"}
            )
        except TokenError:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=['auth'],
    summary='Change password endpoint',
    description='Change the password for the authenticated client',
    request=ClientChangePasswordSerializer,
    responses={
        200: "Password has been changed successfully.",
        400: "Invalid old password or new passwords do not match.",
        401: "Unauthorized request."
    }
)
class ClientChangePasswordView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ClientChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": "The old password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {"detail": "Password has been changed successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)