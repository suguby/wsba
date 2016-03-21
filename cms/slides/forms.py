#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms.widgets import HiddenInput
from django.forms import ModelForm, ModelChoiceField, SlugField

from presentations.models import CoreSlide


class SlideForm(ModelForm):
    # question = ModelChoiceField(label="Вопрос", queryset=Question.objects.all(), widget=HiddenInput())
    # slug = SlugField()

    class Meta:
        model = CoreSlide
        fields = '__all__'
