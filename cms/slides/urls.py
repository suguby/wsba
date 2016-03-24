#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from cms.slides.views import SlideCreateView, SlideDeleteView, SlideUpdateView
from cms.slides.views import  slide_down, slide_up

urlpatterns = [
    url(r'^new/$', login_required(SlideCreateView.as_view()), name='slides_add'),
    url(r'^(?P<slide>[0-9]+)/update/$', login_required(SlideUpdateView.as_view()), name='slides_edit'),
    url(r'^(?P<slide>[0-9]+)/delete/$', login_required(SlideDeleteView.as_view()), name='slides_delete'),
    url(r'^(?P<slide>[0-9]+)/up/$', slide_up, name='slides_up'),
    url(r'^(?P<slide>[0-9]+)/down/$', slide_down, name='slides_down'),

]
