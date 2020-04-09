from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from butter import views
from django.conf.urls import include

urlpatterns = [
    path('', views.api_root),
    path('counties/', 
        views.CountyList.as_view(),
        name='county-list'),
    path('counties/<int:pk>/', 
        views.CountyDetail.as_view(),
        name='county-detail'),
    path('days/', 
        views.DayList.as_view(),
        name='day-list'),
    path('days/<int:pk>/', 
        views.DayDetail.as_view(),
        name='day-detail'),
    path('users/', 
        views.UserList.as_view(),
        name='user-list'),
    path('users/<int:pk>/', 
        views.UserDetail.as_view(),
        name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
