from django.db import models
from django.utils import timezone
from django.conf import settings


def default_pause_title():
    months_in_french = {
        1: "Janvier",
        2: "Février",
        3: "Mars",
        4: "Avril",
        5: "Mai",
        6: "Juin",
        7: "Juillet",
        8: "Août",
        9: "Septembre",
        10: "Octobre",
        11: "Novembre",
        12: "Décembre",
    }
    now = timezone.now()
    return f"Pause du {now.day} {months_in_french[now.month]} {now.year}"


class Pause(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pauses"
    )
    title = models.CharField("Titre", max_length=200, default=default_pause_title)
    created_at = models.DateTimeField("Créée le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifiée le", auto_now=True)
    empty_your_bag = models.TextField("Vide ton sac", blank=True, default="")
    observation = models.TextField("Observation")

    feelings = models.ManyToManyField("Feeling", related_name="pauses", blank=True)
    needs = models.ManyToManyField("Need", related_name="pauses", blank=True)

    class Meta:
        verbose_name = "Pause empathique"
        verbose_name_plural = "Pauses empathiques"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Pause de {self.user} - {self.created_at.strftime('%d/%m/%Y')}"


class Feeling(models.Model):

    class FeelingFamily(models.TextChoices):
        AFFECTION = "AF", "Affection"
        SERENITE = "SE", "Sérénité"
        JOIE = "JO", "Joie"
        INTERET = "IN", "Intérêt"
        ENERGIE = "EN", "Energie"
        PEUR = "PE", "Peur"
        COLERE = "CO", "Colère"
        TRISTESSE = "TR", "Tristesse"
        CONFUSION = "CF", "Confusion"
        FATIGUE = "FA", "Fatigue"
        SIDERATION = "SI", "Sidération"
        TENSION = "TE", "Tension"

    feeling_family = models.CharField(
        max_length=4,
        choices=FeelingFamily.choices,
        null=False,
        blank=False,
        verbose_name="Famille d'émotions",
        help_text="Famille d'émotions",
    )
    feminine_name = models.CharField("Au féminin", max_length=100)
    masculine_name = models.CharField("Au masculin", max_length=100)

    def __str__(self):
        return self.feminine_name

    def get_label(self, user):
        if hasattr(user, "gender") and user.gender == "M":
            return self.masculine_name
        return self.feminine_name


class Need(models.Model):

    class NeedFamily(models.TextChoices):
        SURVIE = "SU", "Survie"
        INTEGRITE = "IN", "Intégrité"
        REALISATION = "RE", "Réalisation"
        HARMONIE = "HA", "Harmonie"
        RELATION = "RL", "Relation"
        COOPERATION = "CO", "Coopération"
        CELEBRATION = "CE", "Célébration"

    need_family = models.CharField(
        max_length=4,
        choices=NeedFamily.choices,
        null=False,
        blank=False,
        verbose_name="Famille de besoins",
        help_text="Famille de besoins",
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
