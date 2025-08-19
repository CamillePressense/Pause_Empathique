from django.db import models
from django.conf import settings

class Pause(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pauses"
    )

    created_at = models.DateTimeField('Créée le', auto_now_add=True)
    updated_at = models.DateTimeField('Modifiée le', auto_now=True)
    empty_your_bag = models.TextField('Vide ton sac', blank=True, default="")
    observation = models.TextField('Observation')

    def __str__(self):
        return f"Pause de {self.user} - {self.created_at.strftime('%d/%m/%Y')}"

class Feeling(models.Model):

    class FeelingFamily(models.TextChoices):
        AFFECTION = 'AF', 'Affection'
        SERENITE = 'SE', 'Sérénité'
        JOIE = 'JO', 'Joie'
        INTERET = 'IN', 'Intérêt'
        ENERGIE = 'EN', 'Energie'
        PEUR = 'PE', 'Peur'
        COLERE = 'CO', 'Colère'
        TRISTESSE = 'TR', 'Tristesse'
        CONFUSION = 'CF', 'Confusion'
        FATIGUE = 'FA', 'Fatigue'
        SIDERATION = 'SI', 'Sidération'
        TENSION = 'TE', 'Tension'

    feminine_name = models.CharField(max_length=100)
    masculine_name = models.CharField(max_length=100)
    feeling_family =  models.CharField(
        max_length=4,
        choices=FeelingFamily.choices,
        verbose_name='Famille d\'émotions',
        help_text='Famille d\'émotions'    
    )

    def __str__(self):
        return self.feminine_name
    
    def get_label(self, user):
        if hasattr(user, "gender") and user.gender == "M":
            return self.masculine_name
        return self.feminine_name


class Need(models.Model):

    class NeedFamily(models.TextChoices):
        SURVIE = 'SU', 'Survie'
        INTEGRITE = 'IN', 'Intégrité'
        REALISATION = 'RE', 'Réalisation'
        HARMONIE = 'HA', 'Harmonie'
        RELATION = 'RL', 'Relation'
        COOPERATION = 'CO', 'Coopération'
        CELEBRATION = 'CE', 'Célébration'

    name = models.CharField(max_length=100)
    need_family = models.CharField(
        max_length=4,
        choices=NeedFamily.choices,
        verbose_name='Famille de besoins',
        help_text='Famille de besoins'
    )

    def __str__(self):
        return self.name
