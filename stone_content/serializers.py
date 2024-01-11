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
        if obj.general_information.variety_name:
            return obj.general_information.name
        return None

    class Meta:
        model = MineralType
        fields = ["id", "name", "sub_name"]


class CompositionSerializer(SolidModelSerializer):
    mineraltype_compounds = MinimalMineralTypeSerializer(many=True)

    def to_representation(self, instance):
        initial_repr = super(CompositionSerializer, self).to_representation(instance)
        for compound in instance.compounds.split(", "):
            initial_repr["mineraltype_compounds"].append(
                {"id": None, "name": compound, "sub_name": ""}
            )
        return initial_repr

    class Meta:
        model = Composition
        exclude = ["stone", "compounds"]


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
