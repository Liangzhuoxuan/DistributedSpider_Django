from django.contrib import admin
from django.urls import path, include
from .views import index
from compare.views import compare
from compare_two.views import search_by_isbn

urlpatterns = [
    path('index.html', index, name="trackBack"),
    path('user/', include('user.urls')),
    path('compare/', compare, name='compare'),
    path('detail/', include('detail.urls')),
    path('compare_two/', search_by_isbn, name='two_compare'),
]