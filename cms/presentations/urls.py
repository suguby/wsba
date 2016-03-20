#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from cms.questions.views import QuestionListView, QuestionDetailView, QuestionCreateView
from cms.questions.views import QuestionUpdateView, QuestionDeleteView
from cms.presentations.views import PresentationListView


urlpatterns = [
    url(r'^$', login_required(PresentationListView.as_view()), name='presentations-list'),
    url(r'^page/(?P<page>[0-9]+)/$', login_required(QuestionListView.as_view()), name='presentations-list-paginated'),
    url(r'^(?P<presentation>[0-9]+)/$', login_required(QuestionDetailView.as_view()), name='presentations-detail'),
    url(r'^(?P<presentation>[0-9]+)/edit$', login_required(QuestionUpdateView.as_view()), name='presentations-edit'),
    url(r'^(?P<presentation>[0-9]+)/delete$', login_required(QuestionDeleteView.as_view()), name='presentations-delete'),
    url(r'^new/$', login_required(QuestionCreateView.as_view()), name='presentations-add'),
]
