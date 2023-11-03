from solid_backend.utils.serializers import SolidModelSerializer
from rest_framework import serializers

from geomat_content.serializers import MineralTypeSerializer
from .models import Stone, GeneralInformation, Characteristic, Composition, Emergence


class EmergenceSerializer(SolidModelSerializer):
    class Meta:
        model = Emergence
        exclude = ["stone"]


class CompositionSerializer(SolidModelSerializer):
    compounds = serializers.CharField(
        source="get_compounds",
        label=Composition._meta.get_field("compounds").verbose_name
    )
    mineraltype_compounds = MineralTypeSerializer(many=True)

    class Meta:
        model = Composition
        exclude = ["stone"]


class GeneralInformationSerializer(SolidModelSerializer):
    class Meta:
        model = GeneralInformation
        exclude = ["stone"]


class CharacteristcSerializer(SolidModelSerializer):
    class Meta:
        model = Characteristic
        exclude = ["stone"]


class StoneSerializer(SolidModelSerializer):
    general_information = GeneralInformationSerializer()
    characteristics = CharacteristcSerializer()
    composition = CompositionSerializer()
    emergence = EmergenceSerializer()

    class Meta:
        model = Stone
        fields = "__all__"
        depth = 1
