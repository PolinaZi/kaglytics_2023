from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from api.models import Category, Organization, EvaluationMetric, RewardType, Tag


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'kaggle_id', 'name')


class EvaluationMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationMetric
        fields = ('id', 'name')


class RewardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardType
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'kaggle_id', 'name')


class CompetitionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    kaggle_id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    category = CategorySerializer()
    organization = OrganizationSerializer()
    evaluationMetric = EvaluationMetricSerializer()
    maxDailySubmissions = serializers.IntegerField()
    maxTeamSize = serializers.IntegerField()
    rewardType = RewardTypeSerializer()
    rewardQuantity = serializers.IntegerField()
    totalTeams = serializers.IntegerField()
    totalCompetitors = serializers.IntegerField()
    totalSubmissions = serializers.IntegerField()
    enabledDate = serializers.DateTimeField()
    deadline = serializers.DateTimeField()
    # tags = TagSerializer(many=True)
