from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from .models import User
from api.models import Category, Organization, EvaluationMetric, RewardType, Tag, Competition


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    username_error_message = {
        'error': 'The username should only contain alphanumeric characters'}

    password_min_length_error_message = {
        'error': 'Ensure this field has at least 5 characters'}

    password_max_length_error_message = {
        'error': 'Ensure this field has no more than 68 characters'}

    email_exists_error_message = {
        'error': 'User with this email already exists'}

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                self.email_exists_error_message)

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


class CompetitionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Competition
        fields = []  # todo


class EmailVerifySerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['code']


class SignInSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = User.objects.filter(email=email).first()

        if (user is None) or (not user.check_password(password)):
            raise exceptions.AuthenticationFailed({'error': 'Invalid email or password'})

        if not user.is_verified:
            raise exceptions.AuthenticationFailed({'error': 'Your email is not verified. Please verify it'})

        return user.tokens()
