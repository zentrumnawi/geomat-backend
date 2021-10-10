from django.contrib import admin
from django import forms
from solid_backend.photograph.admin import PhotographInline

from .models import MineralType, Cleavage, CrystalSystem, Property, Miscellaneous

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


class CleavageInline(admin.TabularInline):
    model = Cleavage


class MineralTypeAdmin(admin.ModelAdmin):

    list_display = ('name', 'variety',
                    'trivial_name', 'created_at', 'last_modified',
                    'id')
    inlines = [CrystalSystemInline, MiscellaneousInline, PropertyInline, PhotographInline]


admin.site.register(MineralType, MineralTypeAdmin)


class CrystallSystemAdmin(admin.ModelAdmin):
    list_display = ('mineral_type', 'crystal_system', 'temperature',
                    'pressure')


admin.site.register(CrystalSystem, CrystallSystemAdmin)


class CleavageAdmin(admin.ModelAdmin):
    list_display = ("cleavage", "coordinates", "property")


admin.site.register(Cleavage, CleavageAdmin)
