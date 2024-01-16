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
    variety = serializers.SerializerMethodField("get_variety")

    def get_name(self, obj):
        return obj.general_information.name

    def get_variety(self, obj):
        return obj.general_information.variety_name

    class Meta:
        model = MineralType
        fields = ["id", "name", "variety"]


class CompositionSerializer(SolidModelSerializer):
    mineraltype_compounds = MinimalMineralTypeSerializer(many=True)

    def to_representation(self, instance):
        initial_repr = super(CompositionSerializer, self).to_representation(instance)
        if instance.compounds:
            for compound in instance.compounds.split(", "):
                initial_repr["mineraltype_compounds"].append(
                    {"id": None, "name": compound, "variety": ""}
                )
        return initial_repr

    class Meta:
        model = Composition
        exclude = ["stone", "compounds"]


class StoneGeneralInformationSerializer(SolidModelSerializer):
    class Meta:
        model = GeneralInformation
        exclude = ["stone"]

    def to_representation(self, instance):
        _repr = super(StoneGeneralInformationSerializer, self).to_representation(instance)
        _repr["sub_name"] = None
        return _repr


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
        exclude = ["tree_node"]
        depth = 1
