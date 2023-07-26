from .models import Board, Region, Status, Division, Condition
from rest_framework import serializers


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'
#
# class BoardSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Board
#         fields = [
#             'name',
#             'description',
#             'view_count',
#             'price',
#             'count',
#             'photo',
#             'create_at',
#             'update_at',
#             # 'user',
#             'region',
#
#         ]


# class RegionSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Region
#         fields = ['name']

