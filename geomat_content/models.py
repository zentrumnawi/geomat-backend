from django.db import models
from django.contrib.postgres.fields.ranges import DecimalRangeField
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _

from solid_backend.content.models import BaseProfile, TreeNode


class MineralType(BaseProfile):
    """
    Defines the mineral type model.
    """

    LUSTRE_CHOICES = (
        ('AM', _("adamantine lustre")),
        ('DL', _("dull lustre")),
        ('GR', _("greasy lustre")),
        ('MT', _("metallic lustre")),
        ('PY', _("pearly lustre")),
        ('SL', _("silky lustre")),
        ('SM', _("submetallic lustre")),
        ('VT', _("vitreous lustre")),
        ('WY', _("waxy lustre")), )
    FRACTURE_CHOICES = (
        ('CF', _("conchoidal")),
        ('EF', _("earthy")),
        ('HF', _("hackly")),
        ('SF', _("splintery")),
        ('UF', _("uneven")), )

    trivial_name = models.CharField(
        max_length=100, blank=True, verbose_name=_("trivial name"))
    variety = models.CharField(
        max_length=100, blank=True, verbose_name=_("variety"))
    minerals = models.CharField(
        max_length=100, blank=True, verbose_name=_("minerals"))
    mohs_scale = DecimalRangeField(null=True, blank=True)
    density = DecimalRangeField(null=True, blank=True)
    streak = models.CharField(max_length=100, verbose_name=_("streak"))
    normal_color = models.CharField(
        max_length=100, verbose_name=_("normal color"))
    fracture = ArrayField(
        models.CharField(
            max_length=2,
            choices=FRACTURE_CHOICES, ),
        null=True,
        verbose_name=_("fracture"))
    lustre = ArrayField(
        models.CharField(
            max_length=2,
            choices=LUSTRE_CHOICES, ),
        null=True,
        verbose_name=_("lustre"))
    chemical_formula = models.CharField(
        max_length=100, verbose_name=_("chemical formula"))
    other = models.TextField(
        max_length=500, blank=True, verbose_name=_("comment"))
    resource_mindat = models.CharField(
        max_length=100, blank=True, verbose_name=_("MinDat ID"))
    resource_mineralienatlas = models.CharField(
        max_length=100, blank=True, verbose_name=_("MineralienAtlas ID"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created at"))
    last_modified = models.DateTimeField(
        auto_now=True, verbose_name=_("last modified"))

    systematics = models.ForeignKey(
        TreeNode,
        related_name="profiles",
        on_delete=models.DO_NOTHING,
        null=True,
        verbose_name=_("Steckbrief-Ebene"),
    )

    class Meta:
        verbose_name = _("mineral type")
        verbose_name_plural = _("mineral types")

    def __str__(self):
        return self.trivial_name


class Cleavage(models.Model):
    """
    Defines a Cleavage which should be used as a ForeignKey
    inside the Mineraltype Class.
    """

    CLEAVAGE_CHOICES = (
        ('PE', _("perfect")),
        ('LP', _("less perfect")),
        ('GO', _("good")),
        ('DI', _("distinct")),
        ('ID', _("indistinct")),
        ('NO', _("none")), )

    cleavage = models.CharField(
        max_length=2, choices=CLEAVAGE_CHOICES, verbose_name=_("cleavage")
    )

    coordinates = models.CharField(
        max_length=100, default="", blank=True, verbose_name=_("coordinates")
    )

    mineral_type = models.ForeignKey(
        MineralType,
        blank=True,
        null=True,
        verbose_name=_("mineral type"),
        related_name="cleavage",
        on_delete=models.CASCADE
    )
