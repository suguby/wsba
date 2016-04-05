#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from cms.presentations.views import PresentationListView, \
    PresentationCreateView, PresentationDetailView, PresentationUpdateView, \
    PresentationDeleteView


urlpatterns = [
    url(r'^$', PresentationListView.as_view(), name='presentations_list'),
    url(r'^page/(?P<page>[0-9]+)/$', PresentationListView.as_view(),
        name='presentations_list_paginated'),
    url(r'^(?P<presentation>[0-9]+)/$', PresentationDetailView.as_view(),
        name='presentations_detail'),
    url(r'^(?P<presentation>[0-9]+)/edit/$', PresentationUpdateView.as_view(),
        name='presentations_edit'),
    url(r'^(?P<presentation>[0-9]+)/delete$', PresentationDeleteView.as_view(),
        name='presentations_delete'),
    url(r'^new/$', PresentationCreateView.as_view(), name='presentations_add'),
]
