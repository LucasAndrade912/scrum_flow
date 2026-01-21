"""Project member-related business logic."""

from django.core.paginator import Paginator
from django.db import transaction

from ..models import ProjectMember


class ProjectMemberService:
    """Service class for project member-related business logic."""

    @staticmethod
    def get_project_members_page(project, page_number, per_page=10):
        """
        Get paginated project members.

        Args:
            project: Project instance
            page_number: Page number to retrieve
            per_page: Number of members per page (default: 10)

        Returns:
            Page: Paginated members
        """
        members_list = list(project.members.select_related("user").all())
        paginator = Paginator(members_list, per_page)
        return paginator.get_page(page_number)

    @staticmethod
    @transaction.atomic
    def add_member_to_project(project, user):
        """
        Add a member to a project.

        Args:
            project: Project instance
            user: User instance to add as member

        Returns:
            ProjectMember: The created project member instance
        """
        return ProjectMember.objects.create(project=project, user=user)

    @staticmethod
    def get_project_member(member_id, project):
        """
        Get a project member by ID.

        Args:
            member_id: ProjectMember primary key
            project: Project instance

        Returns:
            ProjectMember: The project member instance

        Raises:
            ProjectMember.DoesNotExist: If member not found
        """
        return ProjectMember.objects.get(pk=member_id, project=project)

    @staticmethod
    @transaction.atomic
    def remove_member_from_project(member):
        """
        Remove a member from a project.

        Args:
            member: ProjectMember instance to remove

        Returns:
            str: The username of the removed member
        """
        username = member.user.username
        member.delete()
        return username
