from django.contrib import admin
from .models import Stone, GeneralInformation


class GeneralInformationInline(admin.TabularInline):
    model = GeneralInformation


class StoneAdmin(admin.ModelAdmin):
    inlines = [ GeneralInformationInline, ]

    class Meta:
        model = Stone


admin.site.register(Stone, StoneAdmin)
admin.site.register(GeneralInformation, admin.ModelAdmin)
# Register your models here.
