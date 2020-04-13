from butter.models import County, Day
from butter.serializers import SpecificCountySerializer, CountySerializer, DaySerializer, UserSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from butter.geosearch import coordinateToFips, zipToFips
from datetime import datetime, date, timedelta
from django.db.models import Sum
from pandas import DataFrame
import numpy


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'counties': reverse('county-list', request=request, format=format),
        'days': reverse('day-list', request=request, format=format)
    })


@api_view(['GET'])
def national_list(request, format=None):
    queryset = Day.objects.values('date').annotate(cases=Sum('cases'), deaths=Sum('deaths'))
    thedate = request.query_params.get('date', None)
    tempset = queryset
    if thedate is not None:
        thedate = datetime.strptime(thedate, '%Y-%m-%d').date()
        queryset = queryset.filter(date=thedate)
    bigset = {'data': queryset}
    show_growth = bool(request.query_params.get('growth', False))
    if show_growth:
        dataset = DataFrame(tempset)
        dataset.set_index('date', inplace=True)
        #deltaset = dataset.shift(1).fillna(0)
        #dataset = dataset - deltaset
        delta = 3
        dataset = dataset.pct_change(periods=delta, fill_method='ffill').replace([numpy.inf], 0).fillna(0)
        if thedate is not None:
            dataset = dataset.loc[[thedate]]
        dataset = dataset.divide(delta)
        dataset = dataset.reset_index(level=['date'])
        growthqueryset = dataset.to_dict('records')
        bigset.update({'growth': growthqueryset})
    return Response([bigset])


@api_view(['GET'])
def day_list(request, format=None):
    queryset = Day.objects.all()
    countycode = request.query_params.get('code', None)
    if countycode is not None:
        thecounty = County.objects.filter(code=countycode)
        if bool(thecounty):
            queryset = queryset.filter(county=thecounty[0])
        else:
            queryset = []
    thedate = request.query_params.get('date', None)
    tempset = DaySerializer(queryset, many=True).data
    if thedate is not None:
        queryset = queryset.filter(date=thedate)
    bigset = {'data': DaySerializer(queryset, many=True).data}
    show_growth = bool(request.query_params.get('growth', False))
    if show_growth:
        dataset = DataFrame(tempset)
        dataset.set_index('date', inplace=True)
        #deltaset = dataset.shift(1).fillna(0)
        #dataset = dataset - deltaset
        delta = 3
        dataset = dataset.pct_change(periods=delta, fill_method='ffill').replace([numpy.inf], 0).fillna(0)
        if thedate is not None:
            dataset = dataset.loc[[thedate]]
        dataset = dataset.divide(delta)
        dataset = dataset.reset_index(level=['date'])
        growthqueryset = dataset.to_dict('records')
        bigset.update({'growth': growthqueryset})
    return Response([bigset])


class DayList(generics.ListCreateAPIView):
    serializer_class = DaySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = Day.objects.all()
        date = self.request.query_params.get('date', None)
        countycode = self.request.query_params.get('code', None)
        if countycode is not None:
            thecounty = County.objects.filter(code=countycode)
            if bool(thecounty):
                queryset = queryset.filter(county=thecounty[0])
            else:
                queryset = []
        if date is not None:
            queryset = queryset.filter(date=date)
        return queryset


class DayDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SlimCountyList(generics.ListCreateAPIView):
    serializer_class = SpecificCountySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = County.objects.all()
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)
        return queryset


class CountyList(generics.ListCreateAPIView):
    serializer_class = CountySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = County.objects.all()
        code = self.request.query_params.get('code', None)
        zipcode = self.request.query_params.get('zip', None)
        lat = self.request.query_params.get('lat', None)
        lon = self.request.query_params.get('long', None)
        if code is not None:
            queryset = queryset.filter(code=code)
        elif zipcode is not None:
            code = zipToFips(zipcode)
            queryset = queryset.filter(code=code)
        elif lat is not None and lon is not None:
            code = coordinateToFips(lat, lon)
            queryset = queryset.filter(code=code)
        return queryset


class CountyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
