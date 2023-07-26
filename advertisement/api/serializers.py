from board import models
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

    def get_user_create(self, obj):
        return obj.user.id



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
