#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from cms.questions.views import QuestionListView, QuestionDetailView,\
    QuestionCreateView
from cms.questions.views import QuestionUpdateView, QuestionDeleteView

urlpatterns = [
    url(r'^$', QuestionListView.as_view(), name='questions_list'),
    url(r'^page/(?P<page>[0-9]+)/$', QuestionListView.as_view(),
        name='questions_list_paginated'),
    url(r'^(?P<question>[0-9]+)/$', QuestionDetailView.as_view(),
        name='questions_detail'),
    url(r'^(?P<question>[0-9]+)/edit$', QuestionUpdateView.as_view(),
        name='questions_edit'),
    url(r'^(?P<question>[0-9]+)/delete$', QuestionDeleteView.as_view(),
        name='questions_delete'),
    url(r'^new/$', QuestionCreateView.as_view(), name='questions_add'),
]
