"""Service layer for UserStory management."""

from scrum_app.models import ProductBacklog, SprintBacklog, UserStory


class UserStoryService:
    """Service class for UserStory business logic."""

    @staticmethod
    def create_user_story_for_product_backlog(project, **kwargs):
        """
        Create a user story for a product backlog.

        Args:
            project: The project to create the user story for
            **kwargs: User story fields (title, description, etc.)

        Returns:
            UserStory: The created user story
        """
        product_backlog, _ = ProductBacklog.objects.get_or_create(project=project)
        print(product_backlog)
        # Remove product_backlog and sprint_backlog from kwargs if present
        kwargs.pop("product_backlog", None)
        kwargs.pop("sprint_backlog", None)

        user_story = UserStory(product_backlog=product_backlog, **kwargs)
        user_story.full_clean()
        user_story.save()

        return user_story

    @staticmethod
    def create_user_story_for_sprint_backlog(sprint, **kwargs):
        """
        Create a user story for a sprint backlog.

        Args:
            sprint: The sprint to create the user story for
            **kwargs: User story fields (title, description, etc.)

        Returns:
            UserStory: The created user story
        """
        sprint_backlog, _ = SprintBacklog.objects.get_or_create(sprint=sprint)

        # Remove product_backlog and sprint_backlog from kwargs if present
        kwargs.pop("product_backlog", None)
        kwargs.pop("sprint_backlog", None)

        user_story = UserStory(sprint_backlog=sprint_backlog, **kwargs)
        user_story.full_clean()
        user_story.save()

        return user_story

    @staticmethod
    def update_user_story(user_story, **kwargs):
        """
        Update a user story.

        Args:
            user_story: The user story to update
            **kwargs: Fields to update

        Returns:
            UserStory: The updated user story
        """
        for key, value in kwargs.items():
            setattr(user_story, key, value)

        user_story.full_clean()
        user_story.save()

        return user_story

    @staticmethod
    def move_to_sprint(user_story, sprint):
        """
        Move a user story from product backlog to sprint backlog.

        Args:
            user_story: The user story to move
            sprint: The sprint to move to

        Returns:
            UserStory: The updated user story
        """
        sprint_backlog, _ = SprintBacklog.objects.get_or_create(sprint=sprint)
        user_story.product_backlog = None
        user_story.sprint_backlog = sprint_backlog
        user_story.full_clean()
        user_story.save()

        return user_story

    @staticmethod
    def move_to_product_backlog(user_story, project):
        """
        Move a user story from sprint backlog to product backlog.

        Args:
            user_story: The user story to move
            project: The project to move to

        Returns:
            UserStory: The updated user story
        """
        product_backlog, _ = ProductBacklog.objects.get_or_create(project=project)
        user_story.sprint_backlog = None
        user_story.product_backlog = product_backlog
        user_story.full_clean()
        user_story.save()

        return user_story

    @staticmethod
    def delete_user_story(user_story):
        """
        Delete a user story.

        Args:
            user_story: The user story to delete
        """
        user_story.delete()

    @staticmethod
    def get_project_from_user_story(user_story):
        """
        Get the project associated with a user story.

        Args:
            user_story: The user story

        Returns:
            Project: The associated project
        """
        if user_story.product_backlog:
            return user_story.product_backlog.project
        return user_story.sprint_backlog.sprint.project
