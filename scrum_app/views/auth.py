"""Authentication and user-related views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from ..forms import CustomUserCreationForm
from ..services import UserService


def register_view(request):
    """View para registro de novos usuários."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = UserService.register_user(form, request)

            # Add every new user to the global 'member' group
            try:
                member_group = Group.objects.get(name="member")
                user.groups.add(member_group)
            except Group.DoesNotExist:
                messages.warning(
                    request,
                    "Conta criada, mas o grupo 'member' não foi encontrado no sistema.",
                )

            messages.success(
                request,
                f"Bem-vindo(a), {user.username}! Sua conta foi criada com sucesso.",
            )
            return redirect("home")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def home_view(request):
    """View da página inicial."""
    return render(request, "home.html")