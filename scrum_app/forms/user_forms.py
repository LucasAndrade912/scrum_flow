"""User-related forms."""

from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """Formulário customizado de criação de usuário com campos adicionais."""

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "seu@email.com"}
        ),
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Seu nome"}
        ),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Seu sobrenome"}
        ),
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Escolha um usuário"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Escolha um usuário"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Digite sua senha"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirme sua senha"}
        )
