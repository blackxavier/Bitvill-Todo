from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class ReadUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "email", "date_joined", "is_active"]


class WriteUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
        ]


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)


class RegistrationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        account = User(email=self.validated_data["email"])
        password = self.validated_data["password"]
        confirm_password = self.validated_data["confirm_password"]

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords must match"},code='authorization')
        else:
            account.set_password(password)
            account.save()
            return account
