# -*- coding: utf-8 -*-

from django.contrib import admin
from user_interface.models import *
from presentations.models import Organisation, Presentation

admin.site.register(ProjectUser)
admin.site.register(Organisation)
admin.site.register(Presentation)