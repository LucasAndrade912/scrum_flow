"""Project-related business logic."""

from django.db import transaction
from django.db.models import Q

from ..models import Project


class ProjectService:
    """Service class for project-related business logic."""

    @staticmethod
    def get_user_projects(user):
        """
        Get all projects where the user is owner OR a project member.

        Args:
            user: User instance

        Returns:
            QuerySet: Projects visible to the user
        """
        return (
            Project.objects.filter(Q(owner=user) | Q(members__user=user))
            .distinct()
            .order_by("-created_at")
        )

    @staticmethod
    def get_project_by_id(project_id):
        """
        Get a project by ID (authorization must be handled in the view).

        Args:
            project_id: Project primary key

        Returns:
            Project: The project instance

        Raises:
            Project.DoesNotExist: If project not found
        """
        return Project.objects.get(pk=project_id)

    @staticmethod
    @transaction.atomic
    def create_project(form, owner):
        """
        Create a new project.

        Args:
            form: ProjectForm with valid data
            owner: User instance (project owner)

        Returns:
            Project: The created project instance
        """
        project = form.save(commit=False)
        project.owner = owner
        project.save()
        return project

    @staticmethod
    @transaction.atomic
    def update_project(form):
        """
        Update an existing project.

        Args:
            form: ProjectForm with valid data and instance

        Returns:
            Project: The updated project instance
        """
        return form.save()

    @staticmethod
    @transaction.atomic
    def delete_project(project):
        """
        Delete a project.

        NOTE: Authorization should be enforced in the view (owner-only).

        Args:
            project: Project instance to delete

        Returns:
            str: The name of the deleted project
        """
        project_name = project.name
        project.delete()
        return project_name

    @staticmethod
    def check_project_access(project, user):
        """
        Check if user has access to a project (owner OR member).

        Args:
            project: Project instance
            user: User instance

        Returns:
            bool: True if user is owner or member, False otherwise
        """
        # is_member already returns True for owner in your model implementation
        return project.is_member(user)