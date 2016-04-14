#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms.widgets import HiddenInput
from django.forms import ModelForm, ModelChoiceField, SlugField
from presentations.models import Presentation
from presentations.models import CoreSlide


class SlideForm(ModelForm):
    presentation = ModelChoiceField(label="Организация",
                                    queryset=Presentation.objects.all(),
                                    widget=HiddenInput())
    slug = SlugField(label='Код', widget=HiddenInput(), required=False)

    class Meta:
        model = CoreSlide
        fields = ['presentation', 'slug', 'image', 'description', 'question']
