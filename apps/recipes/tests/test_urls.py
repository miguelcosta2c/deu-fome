from django.urls import resolve, reverse

from apps.recipes import views


class TestRecipeURLs:
    def test_reverse_homepage(self):
        assert reverse("recipes:homepage") == "/"

    def test_reverse_recipe_list(self):
        assert reverse("recipes:recipe_list") == "/recipes/"

    def test_reverse_recipe_detail(self):
        url = reverse(
            "recipes:recipe_detail", kwargs={"recipe_slug": "bolo-de-cenoura"}
        )
        assert url == "/recipes/bolo-de-cenoura"

    def test_resolve_homepage(self):
        resolver = resolve("/")
        assert resolver.func is views.home_page
        assert resolver.url_name == "homepage"
        assert resolver.app_name == "recipes"

    def test_resolve_recipe_list(self):
        resolver = resolve("/recipes/")
        assert resolver.func is views.recipe_list
        assert resolver.url_name == "recipe_list"

    def test_resolve_recipe_detail(self):
        resolver = resolve("/recipes/bolo-de-cenoura")
        assert resolver.func is views.recipe_detail
        assert resolver.url_name == "recipe_detail"
        assert resolver.kwargs["recipe_slug"] == "bolo-de-cenoura"

    def test_nonexistent_url_returns_404(self, client):
        assert client.get("/nao-existe/").status_code == 404
