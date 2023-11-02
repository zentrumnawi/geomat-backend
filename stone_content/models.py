from django.contrib.postgres.fields import ArrayField, DecimalRangeField
from django.db import models
from enum import Enum

from django.forms import MultipleChoiceField
from solid_backend.content.models import SolidBaseProfile
from solid_backend.utils.drf_spectacular_extensions import MDTextField
from django.utils.translation import ugettext_lazy as _


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((str(i.value), i.name) for i in cls)


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.

    Uses Django 1.9's postgres ArrayField
    and a MultipleChoiceField for its formfield.
    """

    def formfield(self, **kwargs):
        defaults = {
            "form_class": MultipleChoiceField,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)

        return super(ArrayField, self).formfield(**defaults)


class Stone(SolidBaseProfile):

    class Meta:
        verbose_name = _("Stein")
        verbose_name_plural = _("Steine")

    def __str__(self):
        try:
            return self.general_information.name
        except models.ObjectDoesNotExist:
            return super(Stone, self).__str__()


class GeneralInformation(models.Model):
    DUNHAM_CHOICES = ChoiceEnum(
        "DunhamChoices",
        (
            "Mudstone",
            "Wackestone",
            "Packstone",
            "Grainstone",
            "Floatstone",
            "Rudstone",
            "Bafflestone",
            "Bidnstone",
            "Framstone",
        )
    )
    ADD_CLASS_CHOICES = ChoiceEnum(
        "AddClassChoices",
        (
            "fluviatil",
            "flachmarin",
            "limnisch",
            "marin",
            "kontinentalnah",
            "glazigen",
            "glazifuviatil",
            "gravitativ",
            "sedimentär",
            "äolisch",
            "konkretionär",
            "kalkig",
            "kieselig",
            "oranogen",
            "karbonatisch",
            "mergelig",
            "halogenidisch (Salz)",
            "sulfatisch",
            "mafisch",
            "intermediär",
            "felsisch",
        )
    )

    name = models.CharField(max_length=256, verbose_name=_("Gesteinsname"))
    alt_name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Alternativname"))
    eng_name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Englischer Name"))
    dunham_class = ChoiceArrayField(
        models.CharField(
            choices=DUNHAM_CHOICES.choices(), max_length=1, blank=True
        ),
        null=True,
        blank=True,
        verbose_name=_("Dunhamn Klassifikation"),
    )
    add_class = ChoiceArrayField(
        models.CharField(
            choices=ADD_CLASS_CHOICES.choices(), max_length=2, blank=True
        ),
        null=True,
        blank=True,
        verbose_name=_("Zusatz Klassifikation"),
    )
    comment = MDTextField(max_length=512, null=True, blank=True)

    stone = models.OneToOneField(
        to=Stone,
        on_delete=models.CASCADE,
        related_name="general_information",
        verbose_name=_("Stein")
    )

    class Meta:
        verbose_name = _("Allgemein")
        verbose_name_plural = _("Allgemein")


class Characteristic(models.Model):
    SEDIMENT_CHOICES = ChoiceEnum(
        "SedimentaryChoices",
        (
            "homogen",
            "inhomogen",
            "matrixgestützt",
            "komponentengestützt",
            "hohe Rauigkeit",
            "mittlere Rauigkeit",
            "geringe Rauigkeit",
            "sehr geringe Rauigkeit",
            "gute Sortierung",
            "mittlere Sortierung",
            "schlechte Sortierung",
            "unreif",
            "mittelreif",
            "reif",
            "hochreif",
            "feine Schichtung",
            "mittlere Schichtung",
            "grobe Schichtung",
            "undeutliche Schichtung",
            "keine Schichtung",
            "Schrägschichtung",
            "Kreuzschichtung",
            "Rippelschichtung",
            "mit Hohlräumen",
            "mit Poren",
            "Lockergestein",
            "Festgestein",
        )
    )
    IGNEOUS_CHOICES = ChoiceEnum(
        "IgneousChoices",
        (
            "gleichkörnig (Mosaikgefüge)",
            "ungleichkörnig (porphyrisch)",
            "aphyrisch",
            "isotrop (ungerichtet)",
            "leichtes Fließgefüge",
            "leichte Einregelung",
            "geringe Rauigkeit",
            "sehr geringe Rauigkeit",
            "gute Sortierung",
            "mittlere Sortierung",
            "schlechte Sortierung",
            "unreif",
            "mittelreif",
            "reif",
            "hochreif",
            "feine Schichtung",
            "mittlere Schichtung",
            "grobe Schichtung",
            "undeutliche Schichtung",
            "keine Schichtung",
            "Schrägschichtung",
            "Kreuzschichtung",
            "Rippelschichtung",
            "mit Hohlräumen",
            "mit Poren",
            "Lockergestein",
            "Festgestein",
        )
    )
    METAMORPHIC_CHOICES = ChoiceEnum(
        "MetamorphicChoices",
        (
            "porphyroblastisch",
            "nematoblastisch",
            "kataklastisch",
            "mylonitisch",
            "gleichkörnig",
            "holokristallin",
            "massig (ungerichtet)",
            "ungeregelt",
            "schiefrig",
            "gneisig",
        )
    )
    POROSITY_CHOICES = ChoiceEnum(
        "PorosityChoices",
        (
            "keine",
            "sehr gering",
            "gering",
            "mittel",
            "hoch",
            "sehr hoch",
        )
    )
    sed_fabtric = ChoiceArrayField(
        models.CharField(
            choices=SEDIMENT_CHOICES.choices(), max_length=2
        ),
        verbose_name=_("Gefüge (Sediment)"),
    )
    ign_fabric = ChoiceArrayField(
        models.CharField(
            choices=IGNEOUS_CHOICES.choices(), max_length=2, blank=True
        ),
        null=True,
        blank=True,
        verbose_name=_("Gefüge (Magmatit)"),
    )
    meta_fabric = ChoiceArrayField(
        models.CharField(
            choices=METAMORPHIC_CHOICES.choices(), max_length=2, blank=True
        ),
        null=True,
        blank=True,
        verbose_name=_("Gefüge (Metamorphit)"),
    )
    fabric_comment = models.TextField(max_length=256, null=True, blank=True, verbose_name=_("Gefüge Anmerkung"))
    grain_size = models.CharField(max_length= 256, null=True, blank= True, verbose_name=_("Korngröße"))
    color_index = models.CharField(max_length= 256, null=True, blank= True, verbose_name=_("Farbzahl M'"))
    color = models.CharField(max_length= 256, null=True, blank= True, verbose_name=_("Farbe"))
    density = DecimalRangeField(null=True, blank=True, verbose_name=_("Dichte [g/cm³]"))
    porosity = models.CharField(choices=POROSITY_CHOICES.choices(), max_length=11, blank=True, null=True)

    stone = models.OneToOneField(
        to=Stone,
        on_delete=models.CASCADE,
        related_name="characteristics",
        verbose_name=_("Stein")
    )

    class Meta:
        verbose_name = _("Eigenschaften")
        verbose_name_plural = _("Eigenschaften")
