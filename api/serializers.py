from rest_framework import serializers
from .models import User

from api.models import Category, Organization, EvaluationMetric, RewardType, Tag


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    username_error_message = {
        'error': 'The username should only contain alphanumeric characters'}

    password_min_length_error_message = {
        'error': 'Ensure this field has at least 5 characters'}

    password_max_length_error_message = {
        'error': 'Ensure this field has no more than 68 characters'}

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        if len(password) < 5:
            raise serializers.ValidationError(self.password_min_length_error_message)

        if len(password) > 68:
            raise serializers.ValidationError(self.password_max_length_error_message)

        if not username.isalnum():
            raise serializers.ValidationError(self.username_error_message)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


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
