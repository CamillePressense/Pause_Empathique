import logging
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

logger = logging.getLogger(__name__)


class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'w-full my-2 border-b border-gray-400 mb-3',
            'placeholder': 'mon_adresse@email.com',
        }),
    )
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'w-full my-2 border-b border-gray-400',
        }),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email:
            email = email.strip().lower()

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)

            if self.user_cache is None:
                raise ValidationError(
                    "Identifiants invalides. Vérifiez votre email et mot de passe.",
                    code="invalid_login",
                )

            if not self.user_cache.is_active:
                raise ValidationError(
                    "Ce compte est désactivé. Contactez l’administrateur.",
                    code="inactive",
                )
        return cleaned_data

    def get_user(self):
        return self.user_cache


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("firstname", "email", "gender")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autocomplete': 'email', 'placeholder': 'Mon email', 'class': 'w-full my-2 border-b border-gray-400 mb-3',})
        self.fields['firstname'].widget.attrs.update({'placeholder': 'Mon prénom', 'class': 'w-full my-2 border-b border-gray-400 mb-3',})
        self.fields['gender'].widget.attrs.update({'placeholder': 'Je préfère lire les textes au:'})
        self.fields['password1'].widget.attrs.update({'class': 'w-full my-2 border-b border-gray-400 mb-3',})
        self.fields['password2'].widget.attrs.update({'class': 'w-full my-2 border-b border-gray-400 mb-3',})

    def clean_firstname(self):
        firstname = self.cleaned_data.get("firstname")
        if firstname:
            firstname = firstname.strip().capitalize()
        return firstname
