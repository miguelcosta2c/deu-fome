import pytest

from apps.recipes.models import Recipe


@pytest.mark.django_db
def test_recipe_model_creation(recipe_data):
    recipe = Recipe.objects.create(slug="test-recipe", **recipe_data)
    assert recipe.title == "Test Recipe"
    assert recipe.description == "This is a test recipe."
    assert recipe.content == "Step 1: Do this. Step 2: Do that."
    assert recipe.preparation_time == 30
    assert recipe.preparation_time_unit == "minutos"
    assert recipe.servings == 4
    assert recipe.servings_unit == "porções"
    assert recipe.author == recipe_data["author"]


@pytest.mark.django_db
def test_recipe_str_returns_title(recipe_data):
    recipe = Recipe.objects.create(slug="test-recipe", **recipe_data)
    assert str(recipe) == "Test Recipe"


@pytest.mark.django_db
def test_recipe_slug_auto_generated(recipe_data):
    recipe = Recipe.objects.create(**recipe_data)
    assert recipe.slug == "test-recipe"


@pytest.mark.django_db
def test_recipe_slug_unique_on_duplicate_title(recipe_data):
    recipe1 = Recipe.objects.create(**recipe_data)
    recipe2 = Recipe.objects.create(**recipe_data)
    assert recipe1.slug == "test-recipe"
    assert recipe2.slug == "test-recipe-1"


@pytest.mark.django_db
def test_recipe_get_absolute_url(recipe_data):
    recipe = Recipe.objects.create(**recipe_data)
    assert recipe.get_absolute_url() == "/recipes/test-recipe"


@pytest.mark.django_db
def test_recipe_default_units(recipe_data):
    recipe = Recipe.objects.create(**recipe_data)
    assert recipe.preparation_time_unit == "minutos"
    assert recipe.servings_unit == "porções"


@pytest.mark.django_db
def test_recipe_timestamps(recipe_data):
    recipe = Recipe.objects.create(**recipe_data)
    assert recipe.created_at is not None
    assert recipe.updated_at is not None
