from django.contrib import admin
from theroom.models import TheRoom


admin.site.register(
    TheRoom,
    list_display=["id", "title"],
    list_display_links=["id", "title"],
)