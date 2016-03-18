#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from presentations.models import Question


class QuestionForm(ModelForm):

    common = forms.BooleanField(label='Общий', required=False, help_text="Использовать в разных организациях")

    class Meta:
        model = Question
        fields = ['number', 'text', 'answers_type', 'common']
