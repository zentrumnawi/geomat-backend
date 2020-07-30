from django.contrib import admin
from django import forms
from solid_backend.photograph.admin import PhotographInline

from .models import MineralType, Cleavage, CrystalSystem

# Register your models here.


class MineraltypeModelForm(forms.ModelForm):

    fracture = forms.MultipleChoiceField(choices=MineralType.FRACTURE_CHOICES)
    lustre = forms.MultipleChoiceField(choices=MineralType.LUSTRE_CHOICES)

    class Meta:
        model = MineralType
        fields = "__all__"


class CrystalSystemInline(admin.TabularInline):
    model = CrystalSystem


class CleavageInline(admin.TabularInline):
    model = Cleavage


class MineralTypeAdmin(admin.ModelAdmin):

    list_display = ('minerals', 'variety',
                    'trivial_name', 'created_at', 'last_modified',
                    'id')
    form = MineraltypeModelForm
    inlines = [CrystalSystemInline, CleavageInline, PhotographInline]


admin.site.register(MineralType, MineralTypeAdmin)


class CrystallSystemAdmin(admin.ModelAdmin):
    list_display = ('mineral_type', 'crystal_system', 'temperature',
                    'pressure')


admin.site.register(CrystalSystem, CrystallSystemAdmin)


class CleavageAdmin(admin.ModelAdmin):
    list_display = ("cleavage", "coordinates", "mineral_type")


admin.site.register(Cleavage, CleavageAdmin)
