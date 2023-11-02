from solid_backend.utils.serializers import SolidModelSerializer
from .models import Stone, GeneralInformation


class GeneralInformationSerializer(SolidModelSerializer):
    class Meta:
        model = GeneralInformation
        exclude = ["stone"]


class StoneSerializer(SolidModelSerializer):
    general_information = GeneralInformationSerializer()

    class Meta:
        model = Stone
        fields = "__all__"
        depth = 1
