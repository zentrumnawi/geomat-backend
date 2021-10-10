from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from solid_backend.photograph.serializers import PhotographSerializer

from .models import Cleavage, CrystalSystem, MineralType, Property, Miscellaneous


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


class CleavageSerializer(serializers.ModelSerializer):

    cleavage = serializers.SerializerMethodField()

    class Meta:
        model = Cleavage
        fields = ("cleavage", "coordinates")

    def get_cleavage(self, obj):
        return obj.get_cleavage_display()


class CrystalSystemSerializer(serializers.ModelSerializer):
    """
    This Serializer is used to represent a Version without the full mineraltype
    """

    crystal_system = serializers.SerializerMethodField()

    def get_crystal_system(self, obj):
        choice_dict = dict(obj.CRYSTAL_SYSTEM_CHOICES)
        key = obj.crystal_system
        if key:
            return choice_dict[key]

        return key

    class Meta:
        model = CrystalSystem
        fields = ('id', 'mineral_type', 'crystal_system', 'temperature',
                  'pressure')


class PropertySerializer(serializers.ModelSerializer):

    fracture = serializers.SerializerMethodField()
    lustre = serializers.SerializerMethodField()
    density = serializers.SerializerMethodField()
    mohs_scale = serializers.SerializerMethodField()
    cleavage = CleavageSerializer(many=True)
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
    crystal_system = CrystalSystemSerializer(many=True)
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
