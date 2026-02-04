"""Serializers for the Scrum Flow API."""

from django.contrib.auth.models import User
from rest_framework import serializers

from scrum_app.models import Project, ProjectMember


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model."""

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "created_at", "owner"]
