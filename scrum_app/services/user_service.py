"""User-related business logic."""

from django.contrib.auth import login
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from scrum_app.models import Project, ProjectMember, Sprint, Task, UserStory


class UserService:
    """Service class for user-related business logic."""

    @staticmethod
    def grant_basic_permissions(user):
        """
        Grant basic permissions to a new user.

        New users receive only view and add permissions.
        Change and delete permissions are controlled by business logic
        (e.g., project ownership).

        Args:
            user: User instance to grant permissions to
        """
        models = [Project, ProjectMember, Sprint, UserStory, Task]
        permissions = []

        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            # Only grant view and add permissions to new users
            model_permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=[
                    f"view_{model._meta.model_name}",
                    f"add_{model._meta.model_name}",
                ],
            )
            permissions.extend(model_permissions)

        user.user_permissions.add(*permissions)

    @staticmethod
    def grant_all_permissions(user):
        """
        Grant all scrum_app permissions to a user.

        This should be used for administrators or through
        the grant_permissions management command.

        Args:
            user: User instance to grant permissions to
        """
        models = [Project, ProjectMember, Sprint, UserStory, Task]
        permissions = []

        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            model_permissions = Permission.objects.filter(content_type=content_type)
            permissions.extend(model_permissions)

        user.user_permissions.add(*permissions)

    @staticmethod
    def register_user(form, request):
        """
        Register a new user, grant basic permissions, and log them in.

        Args:
            form: CustomUserCreationForm with valid data
            request: HTTP request object

        Returns:
            User: The created user instance
        """
        user = form.save()
        UserService.grant_basic_permissions(user)
        login(request, user)
        return user
