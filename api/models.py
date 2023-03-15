from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Organization(models.Model):
    name = models.CharField(max_length=200)


class EvaluationMetric(models.Model):
    name = models.CharField(max_length=250)


class RewardType(models.Model):
    name = models.CharField(max_length=100)


class Competition(models.Model):
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
    totalCompetitors = models.IntegerField()
    totalSubmissions = models.IntegerField()
    enabledDate = models.DateTimeField()
    deadline = models.DateTimeField()
    tags = models.ManyToManyField(Tag)
