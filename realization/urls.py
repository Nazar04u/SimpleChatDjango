from django.urls import path
from .views import (
    UserRegistrationView,
    ThreadListCreateView,
    ThreadDeleteView,
    MessageListCreateView,
    MarkMessageAsReadView,
    UnreadCountView,
)

urlpatterns = [
    # User registration
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    # Thread URLs
    path("threads/", ThreadListCreateView.as_view(), name="thread-list"),
    path("threads/<int:pk>/", ThreadDeleteView.as_view(), name="thread-detail"),
    # Message URLs
    path(
        "threads/<int:thread_id>/messages/",
        MessageListCreateView.as_view(),
        name="message-list",
    ),
    path(
        "messages/<int:message_id>/mark_as_read/",
        MarkMessageAsReadView.as_view(),
        name="mark-message-as-read",
    ),
    path("messages/unread_count/", UnreadCountView.as_view(), name="unread-count"),
]
