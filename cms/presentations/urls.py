#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from cms.presentations.views import PresentationListView, PresentationCreateView, \
    PresentationDetailView, PresentationUpdateView, PresentationDeleteView


urlpatterns = [
    url(r'^$', login_required(PresentationListView.as_view()), name='presentations_list'),
    url(r'^page/(?P<page>[0-9]+)/$', login_required(PresentationListView.as_view()), name='presentations_list_paginated'),
    url(r'^(?P<presentation>[0-9]+)/$', login_required(PresentationDetailView.as_view()), name='presentations_detail'),
    url(r'^(?P<presentation>[0-9]+)/edit/$', login_required(PresentationUpdateView.as_view()), name='presentations_edit'),
    url(r'^(?P<presentation>[0-9]+)/delete$', login_required(PresentationDeleteView.as_view()),
        name='presentations_delete'),
    url(r'^new/$', login_required(PresentationCreateView.as_view()), name='presentations_add'),
]
