from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    class Gender(models.TextChoices):
        FEMALE = "F", "Féminin"
        MALE = "M", "Masculin"

    email = models.EmailField(
        unique=True,
        verbose_name="Adresse email",
    )

    firstname = models.CharField(
        max_length=150,
        verbose_name="Prénom",
    )

    gender = models.CharField(
        choices=Gender.choices,
        verbose_name="Je préfère lire les textes au",
        help_text="Préférence de genre pour les textes",
    )

    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Date de création"
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Indique si l'utilisateur peut se connecter",
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="Membre du staff",
        help_text="Indique si l'utilisateur peut accéder à l'admin",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname"]

    class Meta:
        verbose_name = "Utilisateur-ice"
        verbose_name_plural = "Utilisateur-ices"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.firstname} ({self.email})"

    def get_full_name(self):
        return self.firstname

    def get_short_name(self):
        return self.firstname
