import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.validators import validar_dimensoes, validar_peso, validar_tipo


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        validators=[validar_peso, validar_tipo, validar_dimensoes],
        verbose_name="Foto de perfil",
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Biografia",
    )

    def __str__(self) -> str:
        return self.username
