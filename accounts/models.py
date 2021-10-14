import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.base import Model
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from accounts.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    is_trusty = models.BooleanField(_('trusty'), default=False, help_text=_('Designates whether this user has confirmed his account.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def get_full_name(self):
        full_name = f'${self.first_name} ${self.last_name}'
        return full_name.strip()
    
    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

class UserAddress(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    street = models.CharField(_('street'), max_length=30)
    number = models.CharField(_('number'), max_length=10)
    complement = models.CharField(_('complement'), max_length=50, blank=True)
    district =  models.CharField(_('district'), max_length=50)
    city =  models.CharField(_('city'), max_length=30)
    state =  models.CharField(_('state'), max_length=20)

    
