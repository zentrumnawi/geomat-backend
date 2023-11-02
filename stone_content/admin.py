from django.contrib import admin
from .models import Stone


class StoneAdmin(admin.ModelAdmin):

    class Meta:
        model = Stone


admin.site.register(Stone, StoneAdmin)
# Register your models here.
