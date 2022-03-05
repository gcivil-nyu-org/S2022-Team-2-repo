from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


@deconstructible
class NetIdValidator(validators.RegexValidator):
    regex = r'^[\w]+\Z'
    message = _('Enter a valid username. This value may contain only letters or numbers')
    flags = 0


class UserDetails(AbstractUser):
    username = None

    netid_validator = NetIdValidator()
    netid = models.CharField(
        _('netid'),
        max_length=10,
        unique=True,
        help_text=_('Required. 10 characters or fewer. Letters and digits only.'),
        validators=[netid_validator],
        error_messages={
            'unique': _("A user with that NetID already exists."),
        },
    )

    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    middle_name = models.CharField(_('middle name'), max_length=150, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active.'
        ),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'netid'
    REQUIRED_FIELDS = []
