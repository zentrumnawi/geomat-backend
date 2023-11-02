from rest_framework import serializers
from solid_backend.media_object.serializers import MediaObjectSerializer
from solid_backend.utils.serializers import SolidModelSerializer
from django.utils.translation import ugettext_lazy as _
from solid_backend.photograph.serializers import PhotographSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer
from drf_yasg import openapi


from .models import Property, Miscellaneous, MineralType, GeneralInformation
from drf_spectacular.utils import extend_schema_field


class VerboseLabelField(serializers.Field):

    def bind(self, field_name, parent):
        super(VerboseLabelField, self).bind(field_name, parent)
        self.label = str(self.parent.Meta.model._meta.get_field(self.field_name).verbose_name)



@extend_schema_field({"type": "colstring"})
class ColStringField(VerboseLabelField, serializers.CharField):
    pass


class CrystalSystemField(serializers.CharField):
    """
    This Serializer is used to represent a Version without the full mineraltype
    """

    def bind(self, field_name, parent):
        super(CrystalSystemField, self).bind(field_name, parent)
        self.label = _("Crystal Systems")

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
class ListVerboseField(VerboseLabelField):

    def __init__(self, choice_dict, **kwargs):
        super(ListVerboseField, self).__init__()
        self.choice_dict = dict(choice_dict)

    # def bind(self, field_name, parent):
    #     super(ListVerboseField, self).bind(field_name, parent)
    #     self.label = str(self.parent.Meta.model._meta.get_field(self.field_name).verbose_name)

    def to_representation(self, value):
        lst = []
        if value:
            lst = [self.choice_dict.get(choice) for choice in value]
        return lst

    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_ARRAY,
            "items": {
                "type": openapi.TYPE_STRING,
            },
        }


class RangeOrSingleNumberField(VerboseLabelField):

    def to_representation(self, value):
        if float(value.upper) == float(value.lower) + 0.001:
            return "{}".format(value.lower).replace(".", ",")
        return "{0} - {1}".format(value.lower, value.upper).replace(".", ",")


class PropertySerializer(serializers.ModelSerializer):

    fracture = ListVerboseField(Property.FRACTURE_CHOICES)
    lustre = ListVerboseField(Property.LUSTRE_CHOICES)
    density = RangeOrSingleNumberField()
    mohs_scale = RangeOrSingleNumberField()
    normal_color = ColStringField()

    class Meta:
        model = Property
        exclude = ["mineral_type", ]
        swagger_schema_fields = {"title": str(model._meta.verbose_name)}


class MiscellaneousSerializer(serializers.ModelSerializer):

    class Meta:
        model = Miscellaneous
        exclude = ["mineral_type", ]
        swagger_schema_fields = {"title": str(model._meta.verbose_name)}


class GeneralInformationSerializer(SolidModelSerializer):
    name = serializers.CharField(source="get_name")
    trivial_name = serializers.CharField(source="get_trivial_name")

    class Meta:
        model = GeneralInformation
        exclude = ["mineral_type"]


class MineralTypeSerializer(serializers.ModelSerializer):
    general_information = GeneralInformationSerializer()
    crystal_system = CrystalSystemField()
    media_objects = MediaObjectSerializer(many=True)
    property = PropertySerializer()
    miscellaneous = MiscellaneousSerializer()

    class Meta:
        model = MineralType
        fields = "__all__"
        depth = 2
