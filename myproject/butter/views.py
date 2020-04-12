from butter.models import County, Day
from butter.serializers import SpecificCountySerializer, CountySerializer, DaySerializer, UserSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from butter.geosearch import coordinateToFips, zipToFips


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'counties': reverse('county-list', request=request, format=format),
        'days': reverse('day-list', request=request, format=format)
    })


class DayList(generics.ListCreateAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = Day.objects.all()
        date = self.request.query_params.get('date', None)
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
