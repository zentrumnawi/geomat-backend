from rest_framework import serializers
from solid_backend.media_object.serializers import MediaObjectSerializer
from django.utils.translation import ugettext_lazy as _
from solid_backend.photograph.serializers import PhotographSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer

from .models import MineralType, Property, Miscellaneous
from drf_spectacular.utils import extend_schema_field
from .models import CrystalSystem, MineralType


class VerboseLabelField:

    def bind(self, field_name, parent):
        super(VerboseLabelField, self).bind(field_name, parent)
        self.label = self.parent.Meta.model._meta.get_field(self.field_name).verbose_name


@extend_schema_field({"type": "mdstring"})
class MdStringField(VerboseLabelField, serializers.CharField):
    pass


@extend_schema_field({"type": "colstring"})
class ColStringField(VerboseLabelField, serializers.CharField):
    pass


class CrystalSystemField(serializers.CharField):
    """
    This Serializer is used to represent a Version without the full mineraltype
    """

    def to_representation(self, value):
        return_str = ""
        for system in value.all():

            return_str += f"{system.get_crystal_system_display()}"
            if system.temperature:
                return_str += system.temperature
            if system.pressure:
                return_str += f"{system.pressure} \n"

        return return_str


@extend_schema_field({"type": "array", "items": {"type": "string"}})
class ListVerboseField(VerboseLabelField, serializers.ListField):

    def __init__(self, choice_dict, **kwargs):
        super(ListVerboseField, self).__init__()
        self.choice_dict = dict(choice_dict)

    def bind(self, field_name, parent):
        super(ListVerboseField, self).bind(field_name, parent)
        self.label = self.parent.Meta.model._meta.get_field(self.field_name).verbose_name

    def to_representation(self, value):
        lst = []
        if value:
            lst = [self.choice_dict.get(choice) for choice in value]
        return lst


class RangeOrSingleNumberField(VerboseLabelField, serializers.CharField):

    def bind(self, field_name, parent):
        super(RangeOrSingleNumberField, self).bind(field_name, parent)
        self.label = self.parent.Meta.model._meta.get_field(self.field_name).verbose_name

    def to_representation(self, value):
        if float(value.upper) == float(value.lower) + 0.001:
            return "{}".format(value.lower).replace(".", ",")
        return "{0} - {1}".format(value.lower, value.upper).replace(".", ",")


class SystematicsField(VerboseLabelField, serializers.CharField):

    def to_representation(self, value):
        if value:
            return value.name
        return None


class PropertySerializer(serializers.ModelSerializer):

    fracture = ListVerboseField(Property.FRACTURE_CHOICES)
    lustre = ListVerboseField(Property.LUSTRE_CHOICES)
    density = serializers.SerializerMethodField()
    mohs_scale = serializers.SerializerMethodField()
    normal_color = ColStringField()
    chemical_formula = MdStringField()

    class Meta:
        model = Property
        exclude = ["mineral_type", ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_density(self, obj):
        if float(obj.density.upper) == float(obj.density.lower) + 0.001:
            return "{}".format(obj.density.lower).replace(".", ",")
        return "{0} - {1}".format(obj.density.lower, obj.density.upper).replace(".", ",")

    @extend_schema_field(OpenApiTypes.STR)
    def get_mohs_scale(self, obj):
        if float(obj.mohs_scale.upper) == float(obj.mohs_scale.lower) + 0.001:
            return "{}".format(obj.mohs_scale.lower).replace(".", ",")
        return "{0} - {1}".format(obj.mohs_scale.lower, obj.mohs_scale.upper).replace(".", ",")


class MiscellaneousSerializer(serializers.ModelSerializer):

    class Meta:
        model = Miscellaneous
        exclude = ["mineral_type", ]


class MineralTypeSerializer(serializers.ModelSerializer):
    systematics = SystematicsField(label=_("systematics"))
    chemical_formula = MdStringField()
    crystal_system = CrystalSystemField()
    media_objects = MediaObjectSerializer(many=True)
    property = PropertySerializer()
    miscellaneous = MiscellaneousSerializer()

    class Meta:
        model = MineralType
        fields = [
            "id", "systematics", "name", "variety", "trivial_name", "chemical_formula",
            "crystal_system", "property", "miscellaneous", "media_objects", "tree_node"
        ]

        depth = 2

    def get_systematics(self, obj):
        systematic = obj.tree_node
        if systematic:
            return systematic.name
        return None
