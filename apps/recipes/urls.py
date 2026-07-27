from django.urls import path

from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.home_page, name="homepage"),
    path("recipes/", views.recipe_list, name="recipe_list"),
    path("recipes/<slug:recipe_slug>", views.recipe_detail, name="recipe_detail"),
]
