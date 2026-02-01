"""Views for UserStory management."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from scrum_app.forms.user_story_forms import MoveUserStoryForm, UserStoryForm
from scrum_app.models import ProductBacklog, Project, Sprint, SprintBacklog, UserStory


@login_required
def product_backlog_view(request, project_pk):
    """View to display the product backlog of a project."""
    project = get_object_or_404(Project, pk=project_pk)

    # Check if user is member or owner
    if not project.is_member(request.user):
        messages.error(request, "Você não tem permissão para acessar este projeto.")
        return redirect("project_list")

    # Get or create product backlog
    product_backlog, _ = ProductBacklog.objects.get_or_create(project=project)

    # Get all user stories in product backlog
    user_stories = product_backlog.user_stories.all()

    context = {
        "project": project,
        "product_backlog": product_backlog,
        "user_stories": user_stories,
    }

    return render(request, "backlog/product_backlog.html", context)


@login_required
def sprint_backlog_view(request, sprint_pk):
    """View to display the sprint backlog of a sprint."""
    sprint = get_object_or_404(Sprint, pk=sprint_pk)
    project = sprint.project

    # Check if user is member or owner
    if not project.is_member(request.user):
        messages.error(request, "Você não tem permissão para acessar esta sprint.")
        return redirect("project_list")

    # Get or create sprint backlog
    sprint_backlog, _ = SprintBacklog.objects.get_or_create(sprint=sprint)

    # Get all user stories in sprint backlog
    user_stories = sprint_backlog.user_stories.all()

    context = {
        "project": project,
        "sprint": sprint,
        "sprint_backlog": sprint_backlog,
        "user_stories": user_stories,
    }

    return render(request, "backlog/sprint_backlog.html", context)


@login_required
def user_story_create_for_product_backlog(request, project_pk):
    """Create a new user story for product backlog."""
    project = get_object_or_404(Project, pk=project_pk)

    # Check if user is member or owner
    if not project.is_member(request.user):
        messages.error(request, "Você não tem permissão para acessar este projeto.")
        return redirect("project_list")

    # Get or create product backlog
    product_backlog, _ = ProductBacklog.objects.get_or_create(project=project)

    if request.method == "POST":
        form = UserStoryForm(request.POST)
        if form.is_valid():
            user_story = form.save(commit=False)
            user_story.product_backlog = product_backlog
            user_story.save()
            messages.success(request, "User Story criada com sucesso!")
            return redirect("product_backlog", project_pk=project.pk)
    else:
        form = UserStoryForm()

    context = {
        "form": form,
        "project": project,
        "backlog_type": "Product Backlog",
    }

    return render(request, "backlog/user_story_form.html", context)


@login_required
def user_story_create_for_sprint_backlog(request, sprint_pk):
    """Create a new user story for sprint backlog."""
    sprint = get_object_or_404(Sprint, pk=sprint_pk)
    project = sprint.project

    # Check if user is member or owner
    if not project.is_member(request.user):
        messages.error(request, "Você não tem permissão para acessar esta sprint.")
        return redirect("project_list")

    # Get or create sprint backlog
    sprint_backlog, _ = SprintBacklog.objects.get_or_create(sprint=sprint)

    if request.method == "POST":
        form = UserStoryForm(request.POST)
        if form.is_valid():
            user_story = form.save(commit=False)
            user_story.sprint_backlog = sprint_backlog
            user_story.save()
            messages.success(request, "User Story criada com sucesso!")
            return redirect("sprint_backlog", sprint_pk=sprint.pk)
    else:
        form = UserStoryForm()

    context = {
        "form": form,
        "project": project,
        "sprint": sprint,
        "backlog_type": "Sprint Backlog",
    }

    return render(request, "backlog/user_story_form.html", context)


@login_required
def user_story_update_view(request, pk):
    """Update an existing user story."""
    user_story = get_object_or_404(UserStory, pk=pk)

    # Get project from backlog
    if user_story.product_backlog:
        project = user_story.product_backlog.project
        backlog_type = "Product Backlog"
    else:
        project = user_story.sprint_backlog.sprint.project
        backlog_type = "Sprint Backlog"

    # Check if user is member or owner
    if not project.is_member(request.user):
        messages.error(request, "Você não tem permissão para editar esta user story.")
        return redirect("project_list")

    if request.method == "POST":
        form = UserStoryForm(request.POST, instance=user_story)
        if form.is_valid():
            form.save()
            messages.success(request, "User Story atualizada com sucesso!")

            # Redirect based on backlog type
            if user_story.product_backlog:
                return redirect("product_backlog", project_pk=project.pk)
            else:
                return redirect(
                    "sprint_backlog", sprint_pk=user_story.sprint_backlog.sprint.pk
                )
    else:
        form = UserStoryForm(instance=user_story)

    context = {
        "form": form,
        "project": project,
        "user_story": user_story,
        "backlog_type": backlog_type,
        "is_update": True,
    }

    return render(request, "backlog/user_story_form.html", context)


@login_required
def user_story_delete_view(request, pk):
    """Delete a user story."""
    user_story = get_object_or_404(UserStory, pk=pk)

    # Get project from backlog
    if user_story.product_backlog:
        project = user_story.product_backlog.project
        redirect_url = "product_backlog"
        redirect_pk = project.pk
    else:
        project = user_story.sprint_backlog.sprint.project
        redirect_url = "sprint_backlog"
        redirect_pk = user_story.sprint_backlog.sprint.pk

    # Check if user is member or owner
    if not project.is_member(request.user):
        messages.error(request, "Você não tem permissão para excluir esta user story.")
        return redirect("project_list")

    if request.method == "POST":
        user_story.delete()
        messages.success(request, "User Story excluída com sucesso!")
        return redirect(
            redirect_url,
            **{
                f"{'project' if redirect_url == 'product_backlog' else 'sprint'}_pk": redirect_pk
            },
        )

    context = {
        "user_story": user_story,
        "project": project,
    }

    return render(request, "backlog/user_story_confirm_delete.html", context)


@login_required
def user_story_detail_view(request, pk):
    """Display user story details."""
    user_story = get_object_or_404(UserStory, pk=pk)

    # Get project from backlog
    if user_story.product_backlog:
        project = user_story.product_backlog.project
    else:
        project = user_story.sprint_backlog.sprint.project

    # Check if user is member or owner
    if not project.is_member(request.user):
        messages.error(
            request, "Você não tem permissão para visualizar esta user story."
        )
        return redirect("project_list")

    context = {
        "user_story": user_story,
        "project": project,
    }

    return render(request, "backlog/user_story_detail.html", context)


@login_required
def user_story_move_view(request, pk):
    """Move a user story between product and sprint backlog."""
    user_story = get_object_or_404(UserStory, pk=pk)

    # Get project from backlog
    if user_story.product_backlog:
        project = user_story.product_backlog.project
    else:
        project = user_story.sprint_backlog.sprint.project

    # Check if user is member or owner
    if not project.is_member(request.user):
        messages.error(request, "Você não tem permissão para mover esta user story.")
        return redirect("project_list")

    if request.method == "POST":
        form = MoveUserStoryForm(request.POST, project=project)
        if form.is_valid():
            move_to = form.cleaned_data["move_to"]

            if move_to == "product":
                user_story.move_to_product_backlog(project)
                messages.success(
                    request, "User Story movida para o Product Backlog com sucesso!"
                )
                return redirect("product_backlog", project_pk=project.pk)
            else:  # sprint
                sprint_id = form.cleaned_data["sprint"]
                sprint = get_object_or_404(Sprint, pk=sprint_id)
                user_story.move_to_sprint(sprint)
                messages.success(
                    request,
                    f"User Story movida para a Sprint '{sprint.name}' com sucesso!",
                )
                return redirect("sprint_backlog", sprint_pk=sprint.pk)
    else:
        # Set initial value based on current backlog
        initial = {"move_to": "sprint" if user_story.product_backlog else "product"}
        form = MoveUserStoryForm(initial=initial, project=project)

    context = {
        "form": form,
        "user_story": user_story,
        "project": project,
    }

    return render(request, "backlog/user_story_move.html", context)
