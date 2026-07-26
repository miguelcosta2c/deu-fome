from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Recipe


# Create your views here.
def recipe_list(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.all()
    context = {"recipes": recipes}
    return render(request, "recipes/recipe_list.html", context)


def recipe_detail(request: HttpRequest, recipe_slug: str) -> HttpResponse:
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    context = {"recipe": recipe}
    return render(request, "recipes/recipe_detail.html", context)
