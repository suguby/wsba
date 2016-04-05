from django import forms
from django.forms import Form


class PrefaceForm(Form):
    Organisation_name = forms.CharField(label='Наименование организации', max_length=150)
