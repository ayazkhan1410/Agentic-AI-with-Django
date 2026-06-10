from rest_framework import serializers
from agents.models import Document
from django.contrib.auth.models import User


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'is_staff', 'is_superuser',
        ]


class DocumentSerializer(serializers.ModelSerializer):
    owner = RetrieveUserSerializer()
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %I:%M:%S %p",
        read_only=True,
    )
    updated_at = serializers.DateTimeField(
        format="%Y-%m-%d %I:%M:%S %p",
        read_only=True,
    )

    class Meta:
        model = Document
        fields = [
            "id",
            "owner",
            "title",
            "content",
            "active",
            "created_at",
            "updated_at",
        ]
