from django.db import models
from solid_backend.content.models import SolidBaseProfile
from django.utils.translation import ugettext_lazy as _


class Stone(SolidBaseProfile):

    class Meta:
        verbose_name = _("Stein")
        verbose_name_plural = _("Steine")
