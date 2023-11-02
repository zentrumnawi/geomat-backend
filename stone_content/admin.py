from django.contrib import admin
from .models import Stone, GeneralInformation, Characteristic, Composition


class CompositionInline(admin.TabularInline):
    model = Composition


class GeneralInformationInline(admin.TabularInline):
    model = GeneralInformation


class CharacteristicInline(admin.TabularInline):
    model = Characteristic


class StoneAdmin(admin.ModelAdmin):
    inlines = [GeneralInformationInline, CharacteristicInline, CompositionInline]

    class Meta:
        model = Stone


admin.site.register(Stone, StoneAdmin)
admin.site.register(GeneralInformation, admin.ModelAdmin)
admin.site.register(Characteristic, admin.ModelAdmin)
admin.site.register(Composition, admin.ModelAdmin)
# Register your models here.
