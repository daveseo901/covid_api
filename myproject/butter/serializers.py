from rest_framework import serializers
from butter.models import County, Day
from django.contrib.auth.models import User


class DaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Day
        fields = ['date', 'cases', 'deaths']


class RecentDaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Day
        fields = ['url', 'cases', 'deaths']


class SpecificCountySerializer(serializers.HyperlinkedModelSerializer):
    recent_cases = serializers.IntegerField(source='recent_day.cases', read_only=True)
    
    class Meta:
        model = County
        fields = ['code', 'recent_cases']

    def create(self, validated_data):
        days_data = validated_data.pop('data')
        county = County.objects.create(**validated_data)
        for day_data in days_data:
            Day.objects.create(county=county, **day_data)
        return county


class CountySerializer(serializers.HyperlinkedModelSerializer):
    data = DaySerializer(many=True)
    
    class Meta:
        model = County
        fields = ['name', 'code', 'data']

    def create(self, validated_data):
        days_data = validated_data.pop('data')
        county = County.objects.create(**validated_data)
        for day_data in days_data:
            Day.objects.create(county=county, **day_data)
        return county


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username']
