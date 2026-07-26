from typing import Any

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.validators import validar_dimensoes, validar_peso, validar_tipo


class Recipe(models.Model):
    title = models.CharField(
        max_length=255, help_text="Título da receita", verbose_name="Título"
    )
    description = models.TextField(
        help_text="Descrição da receita",
        verbose_name="Descrição",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="Slug da receita (gerado automaticamente a partir do título)",
        verbose_name="Slug",
    )
    content = models.TextField(
        help_text="Modo de preparo da receita",
        verbose_name="Modo de preparo",
    )
    preparation_time = models.PositiveIntegerField(
        help_text="Tempo de preparo em minutos",
        verbose_name="Tempo de preparo (minutos)",
    )
    servings = models.PositiveIntegerField(
        help_text="Número de porções", verbose_name="Porções"
    )
    image = models.ImageField(
        upload_to="recipe_images/",
        blank=True,
        null=True,
        help_text="Imagem da receita",
        verbose_name="Imagem",
        validators=[validar_peso, validar_tipo, validar_dimensoes],
    )
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="recipes",
        help_text="Autor da receita",
        verbose_name="Autor",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            base_slug = slugify(self.title) or "recipe"
            slug = base_slug
            count = 1

            while Recipe.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("recipes:recipe_detail", kwargs={"recipe_slug": self.slug})
