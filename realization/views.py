from django.contrib.auth.models import User
from rest_framework import generics, status, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .models import Thread, Message
from .serializers import (
    ThreadSerializer,
    MessageSerializer,
    UserRegistrationSerializer,
    MarkMessageAsReadSerializer,
)
from .pagination import MessagePagination, ThreadPagination


class UserRegistrationView(generics.CreateAPIView):
    """User Registration View.

    Allows new users to register by providing a username and password.
    Only accessible to unauthenticated users.
    """
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """Create a new user and return the user ID and username."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED
        )


class ThreadListCreateView(generics.ListCreateAPIView):
    """Thread List and Create View.

    Allows authenticated users to list and create threads.
    Only accessible to authenticated users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ThreadSerializer
    pagination_class = ThreadPagination

    def get_queryset(self):
        """Return threads for the authenticated user."""
        return Thread.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """Create a new thread with two participants.

        Validates that exactly two participants are provided and that the user is one of them.
        """
        participant_ids = self.request.data.get("participants", [])
        if len(participant_ids) != 2:
            raise serializers.ValidationError(
                {"error": "A thread must have exactly 2 participants."}  # Validate participant count
            )

        participants = User.objects.filter(id__in=participant_ids)
        if participants.count() != 2:
            raise serializers.ValidationError(
                {"error": "Both participants must be valid users."}  # Validate participants
            )

        if self.request.user not in participants:
            raise serializers.ValidationError(
                {"error": "You cannot create this thread"}  # Ensure the user is one of the participants
            )

        existing_thread = Thread.objects.filter(
            participants__id=participant_ids[0]
        ).filter(participants__id=participant_ids[1])  # Check for existing threads with the same participants
        if existing_thread.exists():
            serializer.instance = existing_thread.first()  # Reuse the existing thread if it exists
        else:
            thread = Thread.objects.create()
            thread.participants.set(participants)
            serializer.instance = thread
            serializer.save()

        return Response(
            ThreadSerializer(serializer.instance).data, status=status.HTTP_201_CREATED
        )


class ThreadDeleteView(generics.DestroyAPIView):
    """Thread Delete View.

    Allows authenticated users to delete threads they participate in.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ThreadSerializer

    def get_queryset(self):
        """Retrieve the thread to be deleted."""
        pk = self.kwargs["pk"]
        queryset = Thread.objects.filter(id=pk)
        threads = Thread.objects.filter(participants__in=[self.request.user])
        if queryset.exists() and queryset.first() in threads:
            return queryset
        raise serializers.ValidationError({"error": "You can not access this thread"})


class MessageListCreateView(generics.ListCreateAPIView):
    """Message List and Create View.

    Allows authenticated users to list and create messages within a specified thread.
    Only accessible to authenticated users.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    pagination_class = MessagePagination

    def get_queryset(self):
        """Return messages for the specified thread if the user is a participant."""
        thread_id = self.kwargs["thread_id"]
        user = self.request.user

        thread = Thread.objects.filter(id=thread_id, participants=user).first()
        if not thread:
            raise serializers.ValidationError(
                {"error": "You do not have access to this thread"}
            )

        return Message.objects.filter(thread_id=thread_id)

    def perform_create(self, serializer):
        """Assign the thread and sender to the message automatically."""
        thread_id = self.kwargs["thread_id"]
        user = self.request.user

        thread = Thread.objects.filter(id=thread_id, participants=user).first()
        if not thread:
            raise serializers.ValidationError(
                {"error": "You cannot send a message in this thread"}
            )

        serializer.save(thread=thread, sender=user, is_read=True)


class MarkMessageAsReadView(generics.UpdateAPIView):
    """Mark Message as Read View.

    Allows authenticated users to mark messages as read.
    Users cannot mark their own messages as read.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MarkMessageAsReadSerializer

    def get_object(self):
        """Retrieve the message to be marked as read."""
        message_id = self.kwargs["message_id"]
        return get_object_or_404(
            Message, pk=message_id, thread__participants=self.request.user
        )

    def update(self, request, *args, **kwargs):
        """Mark the message as read."""
        message = self.get_object()
        if message.sender == request.user:
            return Response(
                {"error": "You cannot mark your own message as read"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message.is_read = True
        message.save(update_fields=["is_read"])

        return Response({"status": "Message marked as read"}, status=status.HTTP_200_OK)


class UnreadCountView(APIView):
    """Unread Count View.

    Returns the count of unread messages for the authenticated user.
    Only accessible to authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get the count of unread messages for the user."""
        user = request.user

        threads = Thread.objects.filter(participants=user)

        if not threads.exists():
            raise serializers.ValidationError(
                {"error": "You cannot access this thread"}
            )

        unread_count = Message.objects.filter(
            thread__in=threads,
            is_read=False,
        ).exclude(sender=user)

        return Response(
            {"unread_count": unread_count.count()}, status=status.HTTP_200_OK
        )
