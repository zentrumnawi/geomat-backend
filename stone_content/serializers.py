from solid_backend.media_object.serializers import MediaObjectSerializer
from solid_backend.utils.serializers import SolidModelSerializer
from rest_framework import serializers

from geomat_content.models import MineralType
from geomat_content.serializers import MineralTypeSerializer
from .models import Stone, GeneralInformation, Characteristic, Composition, Emergence


class EmergenceSerializer(SolidModelSerializer):
    class Meta:
        model = Emergence
        exclude = ["stone"]


class MinimalMineralTypeSerializer(MineralTypeSerializer):
    name = serializers.SerializerMethodField("get_name")
    sub_name = serializers.SerializerMethodField("get_sub_name")

    def get_name(self, obj):
        return obj.general_information.name

    def get_sub_name(self, obj):
        return obj.general_information.sub_name

    class Meta:
        model = MineralType
        fields = ["id", "name", "sub_name"]


class CompositionSerializer(SolidModelSerializer):
    compounds = serializers.CharField(
        source="get_compounds",
        label=Composition._meta.get_field("compounds").verbose_name
    )
    mineraltype_compounds = MinimalMineralTypeSerializer(many=True)

    class Meta:
        model = Composition
        exclude = ["stone"]


class StoneGeneralInformationSerializer(SolidModelSerializer):
    class Meta:
        model = GeneralInformation
        exclude = ["stone"]


class CharacteristcSerializer(SolidModelSerializer):
    class Meta:
        model = Characteristic
        exclude = ["stone"]


class StoneSerializer(SolidModelSerializer):
    general_information = StoneGeneralInformationSerializer()
    characteristics = CharacteristcSerializer()
    composition = CompositionSerializer()
    emergence = EmergenceSerializer()
    media_objects = MediaObjectSerializer(many=True)

    class Meta:
        model = Stone
        fields = "__all__"
        depth = 1
