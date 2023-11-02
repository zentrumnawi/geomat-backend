from django.contrib import admin
from .models import Stone, GeneralInformation, Characteristic


class GeneralInformationInline(admin.TabularInline):
    model = GeneralInformation


class CharacteristicInline(admin.TabularInline):
    model = Characteristic


class StoneAdmin(admin.ModelAdmin):
    inlines = [GeneralInformationInline, CharacteristicInline]

    class Meta:
        model = Stone


admin.site.register(Stone, StoneAdmin)
admin.site.register(GeneralInformation, admin.ModelAdmin)
admin.site.register(Characteristic, admin.ModelAdmin)
# Register your models here.
