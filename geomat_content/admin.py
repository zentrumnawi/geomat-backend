from django.contrib import admin
from django import forms
from solid_backend.media_object.admin import AudioVideoMediaObjectInline, ImageMediaObjectInline

from .models import MineralType, CrystalSystem, Property, Miscellaneous

# Register your models here.


class PropertyModelForm(forms.ModelForm):

    fracture = forms.MultipleChoiceField(choices=Property.FRACTURE_CHOICES)
    lustre = forms.MultipleChoiceField(choices=Property.LUSTRE_CHOICES)

    class Meta:
        model = Property
        fields = "__all__"


class PropertyInline(admin.StackedInline):
    model = Property
    form = PropertyModelForm


class MiscellaneousInline(admin.StackedInline):
    model = Miscellaneous


class CrystalSystemInline(admin.TabularInline):
    model = CrystalSystem


class MineralTypeAdmin(admin.ModelAdmin):

    list_display = ('name', 'variety',
                    'trivial_name', 'created_at', 'last_modified',
                    'id')
    inlines = [
        CrystalSystemInline,
        MiscellaneousInline,
        PropertyInline,
        ImageMediaObjectInline,
        AudioVideoMediaObjectInline
    ]


admin.site.register(MineralType, MineralTypeAdmin)


class CrystallSystemAdmin(admin.ModelAdmin):
    list_display = ('mineral_type', 'crystal_system', 'temperature',
                    'pressure')


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('mineral_type',)
    form = PropertyModelForm


class MiscellaneousAdmin(admin.ModelAdmin):
    list_display = ('mineral_type', 'resource_mindat', 'resource_mineralienatlas')


admin.site.register(CrystalSystem, CrystallSystemAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Miscellaneous, MiscellaneousAdmin)
