from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Library(models.Model):

    CONNECTORS = [
        ("GMINVENT", "GMInvent"),
        ("C3RB", "C3rb"),
        ("ARCHIMED", "Archimed"),
    ]

    sso_id = models.CharField("Identifiant unique", max_length=20, unique=True)
    name = models.CharField("Nom de la bibliothèque / médiathèque", max_length=255)
    ends_at = models.DateField("Date de fin d'abonnement", null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    connector = models.CharField(
        "Connecteurs",
        choices=CONNECTORS,
        default="GMInvent",
        max_length=20,
    )

    def __str__(self):
        return "{} ({})".format(self.name, self.sso_id)
