#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from cms.views import MainView


urlpatterns = [
    url(r'^$', login_required(MainView.as_view()), name='main'),
]
