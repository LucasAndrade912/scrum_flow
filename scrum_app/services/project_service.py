"""Project-related business logic."""

from django.db import transaction

from ..models import Project


class ProjectService:
    """Service class for project-related business logic."""

    @staticmethod
    def get_user_projects(user):
        """
        Get all projects owned by a user.

        Args:
            user: User instance

        Returns:
            QuerySet: Projects owned by the user
        """
        return Project.objects.filter(owner=user)

    @staticmethod
    def get_project_by_id(project_id, owner):
        """
        Get a project by ID and owner.

        Args:
            project_id: Project primary key
            owner: User instance (project owner)

        Returns:
            Project: The project instance

        Raises:
            Project.DoesNotExist: If project not found
        """
        return Project.objects.get(pk=project_id, owner=owner)

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
        Check if user has access to view project members.

        Args:
            project: Project instance
            user: User instance

        Returns:
            bool: True if user is owner or member, False otherwise
        """
        return project.is_member(user) or project.is_owner(user)
