#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from cms.questions.views import QuestionListView, QuestionDetailView, QuestionCreateView, QuestionUpdateView


urlpatterns = [
    url(r'^$', login_required(QuestionListView.as_view()), name='questions-list'),
    url(r'^(?P<pk>[0-9]+)/$', login_required(QuestionDetailView.as_view()), name='questions-detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', login_required(QuestionUpdateView.as_view()), name='questions-update'),
    url(r'^new/$', login_required(QuestionCreateView.as_view()), name='questions-add'),
]
