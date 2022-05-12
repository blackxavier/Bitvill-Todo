from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from django.db import transaction
from rest_framework.generics import UpdateAPIView
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from accounts.serializers import (
    WriteUserProfileSerializer,
    ReadUserProfileSerializer,
    RegistrationSerializer,
    ChangePasswordSerializer,MyAuthTokenSerializer
)

User = get_user_model()


@transaction.atomic
@api_view(
    [
        "POST",
    ]
)
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():

            account = serializer.save()

            data = {
                "user": {
                    "email": account.email,
                },
                "response": "Account was successfuly created",
                "status": f"{status.HTTP_201_CREATED} CREATED",
            }
            return Response(data)
        else:
            data = serializer.errors
            return Response(data)


class ObtainAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = MyAuthTokenSerializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, created = Token.objects.get_or_create(user=user)
        print(token.key)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


# ---------------


class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # confirm the new passwords match

            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response(
                    {"new_password": ["New passwords does not match"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"response": "successfully changed password"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------


@transaction.atomic
@api_view(["GET", "PUT", "PATCH"])
@permission_classes((permissions.IsAuthenticated,))
def UserProfileView(request):

    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ReadUserProfileSerializer(account)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = WriteUserProfileSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["response"] = "Account update successfully"
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        serializer = WriteUserProfileSerializer(
            account, data=request.data, partial=True
        )
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["response"] = "Account update successfully"
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):

    request.user.auth_token.delete()

    logout(request)
    data = {
        "response": "User logged out successfully.",
        "status": f"{status.HTTP_200_OK} OK",
    }
    return Response(data)
