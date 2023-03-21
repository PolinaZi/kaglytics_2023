from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)


class Tag(models.Model):
    kaggle_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Organization(models.Model):
    kaggle_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200)


class EvaluationMetric(models.Model):
    name = models.CharField(max_length=250)


class RewardType(models.Model):
    name = models.CharField(max_length=100)


class Competition(models.Model):
    kaggle_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.SET_NULL)
    evaluationMetric = models.ForeignKey(EvaluationMetric, null=True, on_delete=models.SET_NULL)
    maxDailySubmissions = models.IntegerField(verbose_name='Цена')
    maxTeamSize = models.IntegerField(verbose_name='Цена')
    rewardType = models.ForeignKey(RewardType, null=True, on_delete=models.SET_NULL)
    rewardQuantity = models.IntegerField(default=0)
    totalTeams = models.IntegerField()
    totalCompetitors = models.IntegerField(null=True, blank=True)
    totalSubmissions = models.IntegerField(null=True, blank=True)
    enabledDate = models.DateTimeField()
    deadline = models.DateTimeField()
    tags = models.ManyToManyField(Tag)


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=False, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        return ''


class VerifyCode(models.Model):
    code = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

