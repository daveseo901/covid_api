from rest_framework import serializers
from butter.models import County, Day
from django.contrib.auth.models import User


class DaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Day
        fields = ['url', 'date', 'cases', 'deaths']


class CountySerializer(serializers.HyperlinkedModelSerializer):
    days = DaySerializer(many=True)
    
    class Meta:
        model = County
        fields = ['url', 'name', 'code', 'days']

    def create(self, validated_data):
        days_data = validated_data.pop('days')
        county = County.objects.create(**validated_data)
        for day_data in days_data:
            Day.objects.create(county=county, **day_data)
        return county


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username']
