#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from cms.questions.views import QuestionListView


urlpatterns = [
    url(r'^$', login_required(QuestionListView.as_view()), name='questions-list'),
]
