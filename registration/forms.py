# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField, CharField, HiddenInput


class MyUserCreationForm(UserCreationForm):
    email = EmailField(max_length=254, required=True)
    next = CharField(max_length=254, required=True, widget=HiddenInput)

    class Meta:
        model = User
        fields = ("username", )
