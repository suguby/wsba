from django import forms
from django.forms import Form


class PrefaceForm(Form):
    error_css_class = 'form-group has-warning has-feedback'
    required_css_class = 'form-group has-warning has-feedback'
    Organisation_name = forms.CharField(label='Наименование организации', max_length=150)
