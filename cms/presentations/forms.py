#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import ModelForm, ModelChoiceField, HiddenInput, SlugField
from presentations.models import Presentation, Organisation


class PresentationForm(ModelForm):
    organisation = ModelChoiceField(label="Организация",
                                    queryset=Organisation.objects.all(),
                                    widget=HiddenInput())
    slug = SlugField(label='Код', widget=HiddenInput(), required=False)

    class Meta:
        model = Presentation
        fields = '__all__'
