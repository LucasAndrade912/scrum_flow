"""Project member management views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import AddMemberForm
from ..models import Project, ProjectMember
from ..services import ProjectMemberService, ProjectService


@login_required
def project_members_view(request, pk):
    """View to list all members of a project with pagination."""
    project = get_object_or_404(Project, pk=pk)

    # Check if user is member or owner
    if not ProjectService.check_project_access(project, request.user):
        messages.error(
            request, "Você não tem permissão para ver os membros deste projeto."
        )
        return redirect("project_list")

    # Get paginated members
    page_number = request.GET.get("page")
    members_page = ProjectMemberService.get_project_members_page(project, page_number)

    return render(
        request,
        "projects/project_members.html",
        {
            "project": project,
            "members_page": members_page,
            "is_owner": project.is_owner(request.user),
        },
    )


@login_required
def project_add_member_view(request, pk):
    """View to add a member to a project. Only owner can add members."""
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if request.method == "POST":
        form = AddMemberForm(request.POST, project=project)
        if form.is_valid():
            user = form.cleaned_data["user"]
            ProjectMemberService.add_member_to_project(project, user)
            messages.success(request, f"{user.username} foi adicionado ao projeto!")
            return redirect("project_members", pk=project.pk)
    else:
        form = AddMemberForm(project=project)

    return render(
        request,
        "projects/project_add_member.html",
        {
            "project": project,
            "form": form,
        },
    )


@login_required
def project_remove_member_view(request, pk, member_id):
    """View to remove a member from a project. Only owner can remove members."""
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    member = get_object_or_404(ProjectMember, pk=member_id, project=project)

    if request.method == "POST":
        username = ProjectMemberService.remove_member_from_project(member)
        messages.success(request, f"{username} foi removido do projeto!")
        return redirect("project_members", pk=project.pk)

    return render(
        request,
        "projects/project_remove_member.html",
        {
            "project": project,
            "member": member,
        },
    )
