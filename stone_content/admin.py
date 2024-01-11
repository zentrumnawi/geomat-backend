from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
from solid_backend.media_object.admin import ImageMediaObjectInline, AudioVideoMediaObjectInline

from .models import Stone, GeneralInformation, Characteristic, Composition, Emergence


class MineralTypeSelectField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.general_information.name + ", " + obj.general_information.variety_name


class CompositionAdminForm(ModelForm):
    class Meta:
        model = Composition
        fields = "__all__"
        field_classes = {
            "mineraltype_compounds": MineralTypeSelectField
        }


class EmergenceInline(admin.TabularInline):
    model = Emergence


class CompositionInline(admin.TabularInline):
    model = Composition
    form = CompositionAdminForm


class GeneralInformationInline(admin.TabularInline):
    model = GeneralInformation


class CharacteristicInline(admin.TabularInline):
    model = Characteristic


class StoneAdmin(admin.ModelAdmin):
    inlines = [
        GeneralInformationInline,
        CharacteristicInline,
        CompositionInline,
        EmergenceInline,
        ImageMediaObjectInline,
        AudioVideoMediaObjectInline
    ]

    class Meta:
        model = Stone


admin.site.register(Stone, StoneAdmin)
admin.site.register(GeneralInformation, admin.ModelAdmin)
admin.site.register(Characteristic, admin.ModelAdmin)
admin.site.register(Composition, admin.ModelAdmin)
admin.site.register(Emergence, admin.ModelAdmin)
# Register your models here.
