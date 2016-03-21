#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import ModelForm
from presentations.models import Presentation


class PresentationForm(ModelForm):

    class Meta:
        model = Presentation
        fields = ['name']
