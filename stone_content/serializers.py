from solid_backend.utils.serializers import SolidModelSerializer
from .models import Stone, GeneralInformation, Characteristic


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

    class Meta:
        model = Stone
        fields = "__all__"
        depth = 1
