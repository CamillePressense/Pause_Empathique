import logging
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None
    

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email:
            email = email.strip().lower() 

        if email and password:
            try:
                self.user_cache = authenticate(self.request, email=email, password=password)
                if self.user_cache is None:
                    raise ValidationError(
                        "Identifiants invalides. Vérifiez votre email et mot de passe.",
                        code='invalid_login'
                    )

                if not self.user_cache.is_active:
                    raise ValidationError(
                        "Ce compte est désactivé. Contactez l’administrateur.",
                        code='inactive'
                    )

            except Exception as e:
                logger.error(f"[AUTH ERROR] {e}")
                raise ValidationError(
                    "Une erreur interne est survenue. Réessayez plus tard.",
                    code='internal_error'
                )

        return cleaned_data

    def get_user(self):
        return self.user_cache
