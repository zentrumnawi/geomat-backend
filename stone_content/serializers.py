from solid_backend.utils.serializers import SolidModelSerializer
from .models import Stone


class StoneSerializer(SolidModelSerializer):
    class Meta:
        model = Stone
        fields = "__all__"
        depth = 1
