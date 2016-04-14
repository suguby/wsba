# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import RegistrationView

urlpatterns = [
    url(r'^$', RegistrationView.as_view(), name='registration'),
    url('^', include('django.contrib.auth.urls')),
]
