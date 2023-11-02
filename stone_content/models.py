from django.contrib.postgres.fields import ArrayField
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
