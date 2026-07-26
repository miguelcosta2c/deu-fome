from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    search_fields = ("username", "first_name", "last_name", "email", "telefone")
    fieldsets = (
        *UserAdmin.fieldsets,  # pyright: ignore[reportOptionalIterable]
        (
            "Informações Adicionais",
            {
                "fields": (
                    "id",
                    "profile_picture",
                    "bio",
                ),
            },
        ),
    )
    readonly_fields = ("id",)
