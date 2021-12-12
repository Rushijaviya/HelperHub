from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]
        # fields = ["email", "username", "password", "first_name", "last_name"]


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        many=False, slug_field="username", queryset=User.objects.all()
    )
    receiver = serializers.SlugRelatedField(
        many=False, slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Message
        fields = ["sender", "receiver", "message", "timestamp"]
