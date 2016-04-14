# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Organisation, Presentation, ProjectUser, CoreSlide, Question, Answer, UserAnswer


class CoreSlideInline(admin.TabularInline):
    model = CoreSlide
    extra = 3


class CoreSlideAdmin(admin.ModelAdmin):
    list_filter = ['presentation__name']


class PresentationAdmin(admin.ModelAdmin):
    list_filter = ['organisation__name']
    inlines = [CoreSlideInline]


admin.site.register(Presentation, PresentationAdmin)
admin.site.register(CoreSlide, CoreSlideAdmin)
admin.site.register(Organisation)
admin.site.register(ProjectUser)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserAnswer)
