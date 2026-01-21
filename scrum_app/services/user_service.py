"""User-related business logic."""

from django.contrib.auth import login


class UserService:
    """Service class for user-related business logic."""

    @staticmethod
    def register_user(form, request):
        """
        Register a new user and log them in.

        Args:
            form: CustomUserCreationForm with valid data
            request: HTTP request object

        Returns:
            User: The created user instance
        """
        user = form.save()
        login(request, user)
        return user
