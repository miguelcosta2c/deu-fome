import pytest

from apps.users.models import User


@pytest.fixture
def test_user(db) -> User:
    return User.objects.create_user(
        username="testuser", email="testuser@example.com", password="testpassword"
    )


@pytest.fixture
def recipe_data(test_user):
    return {
        "title": "Test Recipe",
        "description": "This is a test recipe.",
        "content": "Step 1: Do this. Step 2: Do that.",
        "preparation_time": 30,
        "preparation_time_unit": "minutos",
        "servings": 4,
        "servings_unit": "porções",
        "author": test_user,
    }
