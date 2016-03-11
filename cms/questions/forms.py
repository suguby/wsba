#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import ModelForm

from presentations.models import Question


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ['number', 'text', 'answers_type']
