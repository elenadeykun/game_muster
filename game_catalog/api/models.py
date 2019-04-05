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

    def get_musts(self):
        user_musts = self.musts.all()
        return user_musts


class Game(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(max_length=1000, null=True)
    release_date = models.DateField(null=True)
    users_rating = models.FloatField(null=True)
    users_views = models.IntegerField(null=True)
    critics_rating = models.FloatField(null=True)
    critics_views = models.IntegerField(null=True)


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    games = models.ManyToManyField(Game, related_name="genres")


class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True)
    games = models.ManyToManyField(Game, related_name="platforms")


class Image(models.Model):
    url = models.URLField()
    game = models.ForeignKey(Game, related_name="image", on_delete=models.CASCADE)


class Must(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='musts')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)

    @property
    def count(self):
        return Must.objects.filter(game_id=self.game).count()

