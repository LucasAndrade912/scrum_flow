"""Project CRUD views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ProjectForm
from ..models import Project
from ..services import ProjectService


def _require_project_member(project: Project, user) -> None:
    """Ensure user belongs to the project (owner or ProjectMember)."""
    if not project.is_member(user):
        raise PermissionDenied


def _require_project_editor(project: Project, user) -> None:
    """Ensure user can manage (edit) within this project.

    Rule:
    - Owner is always allowed
    - Users in Django group 'editor' are allowed (but still must be a project member)
    """
    if project.is_owner(user):
        return
    if user.groups.filter(name="editor").exists():
        return
    raise PermissionDenied


@login_required
@permission_required("scrum_app.view_project", raise_exception=True)
def project_list_view(request):
    """List projects where the current user is owner or member."""
    projects = ProjectService.get_user_projects(request.user)

    paginator = Paginator(projects, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "projects/project_list.html", {"page_obj": page_obj})


@login_required
@permission_required("scrum_app.view_project", raise_exception=True)
def project_detail_view(request, pk):
    """Display project details."""
    project = get_object_or_404(Project, pk=pk)
    _require_project_member(project, request.user)

    can_manage = project.is_owner(request.user) or request.user.groups.filter(
        name="editor"
    ).exists()

    return render(
        request,
        "projects/project_detail.html",
        {"project": project, "can_manage": can_manage},
    )


@login_required
@permission_required("scrum_app.add_project", raise_exception=True)
def project_create_view(request):
    """Create a new project. Allowed: editors (and superuser)."""
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = ProjectService.create_project(form, request.user)
            messages.success(request, f'Projeto "{project.name}" criado com sucesso!')
            return redirect("project_detail", pk=project.pk)
    else:
        form = ProjectForm()

    return render(
        request,
        "projects/project_form.html",
        {"form": form, "title": "Novo Projeto", "button_text": "Criar Projeto"},
    )


@login_required
@permission_required("scrum_app.change_project", raise_exception=True)
def project_update_view(request, pk):
    """Update an existing project. Allowed: owner or editor (if member)."""
    project = get_object_or_404(Project, pk=pk)
    _require_project_member(project, request.user)
    _require_project_editor(project, request.user)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            ProjectService.update_project(form)
            messages.success(request, f'Projeto "{project.name}" atualizado com sucesso!')
            return redirect("project_detail", pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "projects/project_form.html",
        {
            "form": form,
            "title": "Editar Projeto",
            "button_text": "Salvar Alterações",
            "project": project,
        },
    )


@login_required
def project_delete_view(request, pk):
    """Delete a project. Allowed: owner (and superuser)."""
    project = get_object_or_404(Project, pk=pk)

    if not (project.is_owner(request.user) or request.user.is_superuser):
        raise PermissionDenied

    if request.method == "POST":
        project_name = ProjectService.delete_project(project)
        messages.success(request, f'Projeto "{project_name}" excluído com sucesso!')
        return redirect("project_list")

    return render(request, "projects/project_confirm_delete.html", {"project": project})