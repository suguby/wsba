#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from cms.answers.views import AnswerCreateView


# GET /<organisation slug>/cms/questions/1/edit/answers/new
# POST /<organisation slug>/cms/questions/1/edit/answers/create
# GET /<organisation slug>/cms/questions/1/edit/answers/1/edit
# POST /<organisation slug>/cms/questions/1/edit/answers/1/update
# POST /<organisation slug>/cms/questions/1/edit/answers/1/delete

urlpatterns = [
    url(r'^new/$', login_required(AnswerCreateView.as_view()), name='answers-add'),
]
