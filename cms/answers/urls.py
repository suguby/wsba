#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from cms.answers.views import AnswerCreateView, AnswerDeleteView, AnswerUpdateView
from cms.answers.views import answer_up, answer_down


urlpatterns = [
    url(r'^new/$', AnswerCreateView.as_view(), name='answers_add'),
    url(r'^(?P<answer>[0-9]+)/update/$', AnswerUpdateView.as_view(), name='answers_edit'),
    url(r'^(?P<answer>[0-9]+)/delete/$', AnswerDeleteView.as_view(), name='answers_delete'),
    url(r'^(?P<answer>[0-9]+)/up/$', answer_up, name='answers_up'),
    url(r'^(?P<answer>[0-9]+)/down/$', answer_down, name='answers_down'),
]
