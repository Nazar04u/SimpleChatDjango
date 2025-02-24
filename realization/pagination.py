# In your pagination.py file or directly in your views.py

from rest_framework.pagination import LimitOffsetPagination


class MessagePagination(LimitOffsetPagination):
    default_limit = 10


class ThreadPagination(LimitOffsetPagination):
    default_limit = 5
