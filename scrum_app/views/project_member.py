"""Project member management views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import AddMemberForm
from ..models import Project, ProjectMember
from ..services import ProjectMemberService


def _require_project_member(project: Project, user) -> None:
    """User must be owner or an added member (ProjectMember)."""
    if not project.is_member(user):
        raise PermissionDenied


def _require_project_editor(project: Project, user) -> None:
    """Only editors/admin can manage members (within projects they belong to).

    Rule:
    - Superuser is always allowed
    - Owner is always allowed
    - Users in Django group 'editor' are allowed (but must still be project members)
    """
    if user.is_superuser:
        return
    if project.is_owner(user):
        return
    if user.groups.filter(name="editor").exists():
        return
    raise PermissionDenied


@login_required
@permission_required("scrum_app.view_project", raise_exception=True)
def project_members_view(request, pk):
    """List members of a project (allowed: project members)."""
    project = get_object_or_404(Project, pk=pk)
    _require_project_member(project, request.user)

    page_number = request.GET.get("page")
    members_page = ProjectMemberService.get_project_members_page(project, page_number)

    can_manage = request.user.is_superuser or project.is_owner(
        request.user
    ) or request.user.groups.filter(name="editor").exists()

    return render(
        request,
        "projects/project_members.html",
        {
            "project": project,
            "members_page": members_page,
            "can_manage": can_manage,
        },
    )


@login_required
@permission_required("scrum_app.change_project", raise_exception=True)
def project_add_member_view(request, pk):
    """Add a member to a project (allowed: editor/admin within the project)."""
    project = get_object_or_404(Project, pk=pk)
    _require_project_member(project, request.user)
    _require_project_editor(project, request.user)

    if request.method == "POST":
        form = AddMemberForm(request.POST, project=project)
        if form.is_valid():
            user = form.cleaned_data["user"]

            # Ensure the added user can access "view_*" screens
            try:
                member_group = Group.objects.get(name="member")
                user.groups.add(member_group)
            except Group.DoesNotExist:
                # If group was deleted/missing, we still add the membership.
                pass

            ProjectMemberService.add_member_to_project(project, user)
            messages.success(request, f"{user.username} foi adicionado ao projeto!")
            return redirect("project_members", pk=project.pk)
    else:
        form = AddMemberForm(project=project)

    return render(
        request,
        "projects/project_add_member.html",
        {"project": project, "form": form},
    )


@login_required
@permission_required("scrum_app.change_project", raise_exception=True)
def project_remove_member_view(request, pk, member_id):
    """Remove a member from a project (allowed: editor/admin within the project)."""
    project = get_object_or_404(Project, pk=pk)
    _require_project_member(project, request.user)
    _require_project_editor(project, request.user)

    member = get_object_or_404(ProjectMember, pk=member_id, project=project)

    if request.method == "POST":
        username = ProjectMemberService.remove_member_from_project(member)
        messages.success(request, f"{username} foi removido do projeto!")
        return redirect("project_members", pk=project.pk)

    return render(
        request,
        "projects/project_remove_member.html",
        {"project": project, "member": member},
    )