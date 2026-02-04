"""API views for the Scrum Flow application."""

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

from scrum_app.models import Project, ProjectMember
from scrum_app.serializers import ProjectSerializer, UserSerializer


class UserProjectsListView(generics.ListAPIView):
    """
    API view to list all projects for a specific user.

    Returns projects where the user is either the owner or a member.

    URL: /api/users/<user_id>/projects/
    """

    serializer_class = ProjectSerializer

    def get_queryset(self):
        """Get all projects for the specified user."""
        user_id = self.kwargs["user_id"]

        # Get projects where user is owner
        owned_projects = Project.objects.filter(owner_id=user_id)

        # Get projects where user is a member
        member_projects = Project.objects.filter(members__user_id=user_id)

        # Combine and remove duplicates
        return (owned_projects | member_projects).distinct()

    def list(self, request, *args, **kwargs):
        """Override list to add custom error handling."""
        user_id = self.kwargs["user_id"]

        # Check if user exists
        if not User.objects.filter(id=user_id).exists():
            return Response(
                {"error": f"User with id {user_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return super().list(request, *args, **kwargs)


class ProjectUsersListView(generics.GenericAPIView):
    """
    API view to list all users for a specific project.

    Returns the project owner and all members.

    URL: /api/projects/<project_id>/users/
    """

    def get(self, request, project_id):
        """Get all users for the specified project."""
        # Check if project exists
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {"error": f"Project with id {project_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get owner
        owner_data = UserSerializer(project.owner).data
        owner_data["role"] = "owner"
        owner_data["joined_at"] = project.created_at

        # Get members
        members = ProjectMember.objects.filter(project=project).select_related("user")
        members_data = []

        for member in members:
            user_data = UserSerializer(member.user).data
            user_data["role"] = "member"
            user_data["joined_at"] = member.joined_at
            members_data.append(user_data)

        # Combine owner and members
        all_users = [owner_data] + members_data

        return Response(
            {"project_id": project.id, "project_name": project.name, "users": all_users}
        )
