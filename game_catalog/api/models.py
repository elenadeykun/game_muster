from django.conf import settings
from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager
)
from django.db import models
from django.db.models import Count

from .utils import split


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=80)
    email = models.EmailField(max_length=25)
    last_name = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Must(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='musts')
    game_id = models.IntegerField(null=False)

    @staticmethod
    def get_annotated_user_musts(user):
        PART_LENGTH = 10

        user_musts = Must.objects.filter(owner=user)
        if user_musts:
            game_ids = [elem.game_id for elem in user_musts]
            must_games = (Must.objects.all().values('game_id').annotate(count=Count('game_id'))\
                          .filter(game_id__in=game_ids))

            parts = split(list(must_games), PART_LENGTH) if must_games else []
            return parts
        return None
