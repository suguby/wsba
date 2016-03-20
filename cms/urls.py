#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf.urls import url, include
from cms.dashboard.views import DashboardView

urlpatterns = [
    url(r'^$', login_required(DashboardView.as_view()), name='main'),
    url(r'^presentations/', include('cms.presentations.urls')),
    url(r'^questions/', include('cms.questions.urls')),
    url(r'^questions/(?P<question>[0-9]+)/edit/answers/', include('cms.answers.urls')),
]
