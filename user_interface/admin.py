# -*- coding: utf-8 -*-

from django.contrib import admin
from user_interface.models import *
from presentations.models import Organisation, Presentation, CoreSlide

class CoreSlideInline(admin.TabularInline):
    model = CoreSlide
    extra = 3

class CoreSlideAdmin(admin.ModelAdmin):
    list_filter = ['presentation__name']


class PresentationAdmin(admin.ModelAdmin):
    list_filter = ['organisation__name']
    inlines = [CoreSlideInline]

admin.site.register(ProjectUser)
admin.site.register(Organisation)
admin.site.register(Presentation, PresentationAdmin)
admin.site.register(CoreSlide, CoreSlideAdmin)
admin.site.register(UserPresentation)


