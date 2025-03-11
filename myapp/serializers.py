from rest_framework import serializers
from .models import UserProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ["username", "password"]

    def create(self, validated_data):
        from .utils import hash_password

        password = validated_data.pop("password")
        validated_data["password_hash"] = hash_password(password)
        return UserProfile.objects.create(**validated_data)
