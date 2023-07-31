from board import models
from user.models import CustomUser
from rest_framework import serializers


class BoardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_create = serializers.SerializerMethodField()
    photo = serializers.ImageField(required=False)
    photo_icon = serializers.ImageField(read_only=True)
    photo_page = serializers.ImageField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    update_at = serializers.DateTimeField(read_only=True)
    clear_photo = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = models.Board
        fields = (
            'id',
            'name',
            'description',
            'price',
            'count',
            'user',
            'user_create',
            'region',
            'division',
            'condition',
            'status',
            'photo',
            'photo_icon',
            'photo_page',
            'create_at',
            'update_at',
            'clear_photo'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = self.get_field_required()
        self.fields['description'].required = self.get_field_required()
        self.fields['region'].required = self.get_field_required()
        self.fields['division'].required = self.get_field_required()
        self.fields['condition'].required = self.get_field_required()
        self.fields['status'].required = self.get_field_required()

    def get_user_create(self, obj):
        return obj.user.id

    def get_field_required(self):
        if self.context['request'].method == 'POST':
            return True
        else:
            return False

    def create(self, validated_data):
        validated_data.pop('clear_photo')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.region = validated_data.get('region', instance.region)
        instance.division = validated_data.get('division', instance.division)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance


class RegionSerializer(serializers.ModelSerializer):
    board = serializers.SerializerMethodField()

    class Meta:
        model = models.Region
        fields = (
            'id',
            'name',
            'board',
        )

    def get_board(self, obj):
        queryset = models.Board.objects.filter(region__id=obj.id)
        queryset = queryset.filter(status__name='Public')

        return list(queryset.values_list('id', flat=True))


class DivisionSerializer(serializers.ModelSerializer):
    board = serializers.SerializerMethodField()

    class Meta:
        model = models.Division
        fields = (
            'id',
            'name',
            'board',
        )

    def get_board(self, obj):
        queryset = models.Board.objects.filter(region__id=obj.id)
        queryset = queryset.filter(status__name='Public')

        return list(queryset.values_list('id', flat=True))


class ConditionSerializer(serializers.ModelSerializer):
    board = serializers.SerializerMethodField()

    class Meta:
        model = models.Condition
        fields = (
            'id',
            'name',
            'board',
        )

    def get_board(self, obj):
        queryset = models.Board.objects.filter(region__id=obj.id)
        queryset = queryset.filter(status__name='Public')

        return list(queryset.values_list('id', flat=True))


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_authorized = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'password',
            'is_authorized',
            'last_login',
            'created_at',
            'updated_at',
            'is_active',
            'is_superuser',
            'is_staff',


        ]

    def create(self, validated_data):
        validated_data['last_login'] = None
        validated_data['is_active'] = True
        validated_data['is_superuser'] = False
        validated_data['is_staff'] = False
        validated_data['is_authorized'] = False

        instance = super().create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()

        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if password := validated_data.get('password'):
            instance.set_password(password)
        if validated_data.get('email'):
            instance.is_authorized = False
        instance.save()

        return instance
