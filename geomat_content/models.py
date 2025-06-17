from django.db import models
from django.contrib.postgres.fields.ranges import DecimalRangeField
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _

from solid_backend.content.models import SolidBaseProfile, TreeNode
from solid_backend.utils.drf_spectacular_extensions import MDTextField


class MineralType(SolidBaseProfile):
    """
    Defines the mineral type model.
    """

    searchable_fields = [
        "general_information__name",
        "general_information__trivial_name",
    ]

    @classmethod
    def get_optimized_queryset(cls):
        return cls.objects.select_related(
            "general_information",
            "miscellaneous",
            "property",
        ).prefetch_related(
            "crystal_system",
            "media_objects",
        )

    class Meta:
        verbose_name = _("mineral type")
        verbose_name_plural = _("mineral types")

    def __str__(self):
        return self.general_information.name


class GeneralInformation(models.Model):

    mineral_type = models.OneToOneField(
        to=MineralType,
        on_delete=models.CASCADE,
        related_name="general_information",
        verbose_name=_("mineral type"),
    )
    name = models.CharField(max_length=100, blank=True, verbose_name=_("minerals"))
    variety_name = models.CharField(
        max_length=100, blank=True, verbose_name=_("variety")
    )
    trivial_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("trivial name")
    )

    chemical_formula = MDTextField(max_length=100, verbose_name=_("chemical formula"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    last_modified = models.DateTimeField(auto_now=True, verbose_name=_("last modified"))

    class Meta:
        verbose_name = _("general information")
        verbose_name_plural = _("general information")

    def __str__(self):
        return self.trivial_name


class Miscellaneous(models.Model):

    other = models.TextField(max_length=500, blank=True, verbose_name=_("comment"))
    resource_mindat = models.CharField(
        max_length=100, blank=True, verbose_name=_("MinDat ID")
    )
    resource_mineralienatlas = models.CharField(
        max_length=100, blank=True, verbose_name=_("MineralienAtlas ID")
    )
    mineral_type = models.OneToOneField(
        MineralType,
        verbose_name=_("mineral type"),
        related_name="miscellaneous",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Miscellaneous")
        verbose_name_plural = _("Miscellaneous")


class Property(models.Model):
    FRACTURE_CHOICES = (
        ("CF", _("conchoidal")),
        ("EF", _("earthy")),
        ("HF", _("hackly")),
        ("SF", _("splintery")),
        ("UF", _("uneven")),
    )

    LUSTRE_CHOICES = (
        ("AM", _("adamantine lustre")),
        ("DL", _("dull lustre")),
        ("GR", _("greasy lustre")),
        ("MT", _("metallic lustre")),
        ("PY", _("pearly lustre")),
        ("SL", _("silky lustre")),
        ("SM", _("submetallic lustre")),
        ("VT", _("vitreous lustre")),
        ("WY", _("waxy lustre")),
    )

    density = DecimalRangeField(null=True, blank=True, verbose_name=_("density"))
    fracture = ArrayField(
        models.CharField(
            max_length=2,
            choices=FRACTURE_CHOICES,
        ),
        null=True,
        verbose_name=_("fracture"),
    )
    lustre = ArrayField(
        models.CharField(
            max_length=2, choices=LUSTRE_CHOICES, verbose_name=_("lustre")
        ),
        null=True,
        verbose_name=_("lustre"),
    )
    mohs_scale = DecimalRangeField(null=True, blank=True, verbose_name=_("mohs scale"))
    normal_color = models.CharField(max_length=100, verbose_name=_("normal color"))
    streak = models.CharField(max_length=100, verbose_name=_("streak"))
    mineral_type = models.OneToOneField(
        MineralType,
        verbose_name=_("mineral type"),
        related_name="property",
        on_delete=models.CASCADE,
    )
    cleavage_text = models.TextField(null=True, verbose_name=_("Cleavages"))

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")


class CrystalSystem(models.Model):
    """
    Defines a crystal system, which then should be used as a ForeignKey
    inside the MineralType class.
    """

    CRYSTAL_SYSTEM_CHOICES = (
        ("TC", _("Triclinic")),
        ("MC", _("Monoclinic")),
        ("OR", _("Orthorhombic")),
        ("TT", _("Tetragonal")),
        ("TR", _("Trigonal")),
        ("HG", _("Hexagonal")),
        ("CB", _("Cubic")),
        ("AM", _("Amorph")),
    )

    mineral_type = models.ForeignKey(
        MineralType,
        null=True,
        verbose_name=_("mineral type"),
        on_delete=models.CASCADE,
        related_name="crystal_system",
    )
    crystal_system = models.CharField(
        max_length=2,
        blank=True,
        choices=CRYSTAL_SYSTEM_CHOICES,
        verbose_name=_("crystal system"),
    )
    temperature = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("temperature")
    )
    pressure = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("pressure")
    )

    class Meta:
        verbose_name = _("Crystal System")
        verbose_name_plural = _("Crystal Systems")

    def __str__(self):
        return "{} ({})".format(
            self.mineral_type.general_information.name, self.crystal_system
        )
