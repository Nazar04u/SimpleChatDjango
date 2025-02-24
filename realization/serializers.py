from rest_framework import serializers
from .models import Thread, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Thread
        fields = ["id", "participants", "created", "updated"]


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sender_username = serializers.CharField(source="sender.username", read_only=True)
    sender_id = serializers.IntegerField(source="sender.id", read_only=True)
    is_read = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "sender_username",
            "sender_id",
            "text",
            "created",
            "is_read",
        ]

    def create(self, validated_data):
        """Automatically set the sender and is_read fields."""
        request = self.context.get("request")
        if request and request.user:
            validated_data["sender"] = request.user
        validated_data["is_read"] = False
        return super().create(validated_data)


class MarkMessageAsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["is_read"]
        read_only_fields = ["is_read"]
