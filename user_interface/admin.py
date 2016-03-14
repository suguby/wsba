# -*- coding: utf-8 -*-

from django.contrib import admin
from user_interface.models import *
from presentations.models import Organisation, Presentation, CoreSlide

admin.site.register(ProjectUser)
admin.site.register(Organisation)
admin.site.register(Presentation)
admin.site.register(CoreSlide)