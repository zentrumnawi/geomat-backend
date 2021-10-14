from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from solid_backend.photograph.serializers import PhotographSerializer

from .models import CrystalSystem, MineralType, Property, Miscellaneous


class MdStringField(serializers.CharField):

    class Meta:
        swagger_schema_fields = {
            "type": "mdstring"
        }


class ColStringField(serializers.CharField):

    class Meta:
        swagger_schema_fields = {
            "type": "colstring"
        }


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

class PropertySerializer(serializers.ModelSerializer):

    fracture = serializers.SerializerMethodField()
    lustre = serializers.SerializerMethodField()
    density = serializers.SerializerMethodField()
    mohs_scale = serializers.SerializerMethodField()
    normal_color = ColStringField()

    class Meta:
        model = Property
        fields = '__all__'
        depth = 2

    @swagger_serializer_method(serializer_or_field=serializers.ListField)
    def get_fracture(self, obj):
        lst = []
        choice_dict = dict(obj.FRACTURE_CHOICES)
        fracture = obj.fracture
        if fracture:
            lst = [choice_dict.get(choice) for choice in fracture]
        return lst

    @swagger_serializer_method(serializer_or_field=serializers.ListField)
    def get_lustre(self, obj):
        lst = []
        choice_dict = dict(obj.LUSTRE_CHOICES)
        lustre = obj.lustre
        if lustre:
            lst = [choice_dict.get(choice) for choice in lustre]
        return lst

    def get_density(self, obj):
        if float(obj.density.upper) == float(obj.density.lower) + 0.001:
            return "{}".format(obj.density.lower).replace(".", ",")
        return "{0} - {1}".format(obj.density.lower, obj.density.upper).replace(".", ",")

    def get_mohs_scale(self, obj):
        if float(obj.mohs_scale.upper) == float(obj.mohs_scale.lower) + 0.001:
            return "{}".format(obj.mohs_scale.lower).replace(".", ",")
        return "{0} - {1}".format(obj.mohs_scale.lower, obj.mohs_scale.upper).replace(".", ",")


class MiscellaneousSerializer(serializers.ModelSerializer):

    class Meta:
        model = Miscellaneous
        fields = "__all__"


class MineralTypeSerializer(serializers.ModelSerializer):
    systematics = serializers.SerializerMethodField()
    chemical_formula = MdStringField()
    crystal_system = CrystalSystemField()
    photographs = PhotographSerializer(many=True)
    property = PropertySerializer()
    miscellaneous = MiscellaneousSerializer()

    
    class Meta:
        model = MineralType
        fields = ["systematics", "name", "variety", "trivial_name", "chemical_formula", "crystal_system", "property", "miscellaneous", "photographs"]

        depth = 2

    def get_systematics(self, obj):
        systematic = obj.tree_node
        if systematic:
            return systematic.name
        return None
