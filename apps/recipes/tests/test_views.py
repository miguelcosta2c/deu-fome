import pytest
from django.urls import reverse

from apps.recipes.models import Recipe


@pytest.mark.django_db
class TestHomePage:
    def test_status_code(self, client):
        response = client.get(reverse("recipes:homepage"))
        assert response.status_code == 200

    def test_template_used(self, client):
        response = client.get(reverse("recipes:homepage"))
        assert "global/home.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestRecipeListView:
    def test_status_code(self, client):
        response = client.get(reverse("recipes:recipe_list"))
        assert response.status_code == 200

    def test_empty_list_shows_message(self, client):
        response = client.get(reverse("recipes:recipe_list"))
        assert "Nenhuma receita encontrada" in response.content.decode()

    def test_with_recipes(self, client, recipe_data):
        Recipe.objects.create(**recipe_data)
        response = client.get(reverse("recipes:recipe_list"))
        content = response.content.decode()
        assert "Test Recipe" in content
        assert "This is a test recipe." in content


@pytest.mark.django_db
class TestRecipeDetailView:
    def test_valid_slug(self, client, recipe_data):
        recipe = Recipe.objects.create(**recipe_data)
        url = reverse("recipes:recipe_detail", kwargs={"recipe_slug": recipe.slug})
        response = client.get(url)
        assert response.status_code == 200
        content = response.content.decode()
        assert "Test Recipe" in content
        assert "This is a test recipe." in content
        assert "Step 1" in content

    def test_invalid_slug_returns_404(self, client):
        url = reverse(
            "recipes:recipe_detail", kwargs={"recipe_slug": "non-existent-recipe"}
        )
        response = client.get(url)
        assert response.status_code == 404
