# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import RegistrationView, ProfileView

urlpatterns = [
    url(r'^$', RegistrationView.as_view(), name='registration'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url('^', include('django.contrib.auth.urls')),
]
