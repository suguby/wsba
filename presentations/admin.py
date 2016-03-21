# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Organisation, Presentation, ProjectUser, CoreSlide, Question, Answer, UserAnswer


class OrganisationAdmin(admin.ModelAdmin):
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class PresentationAdmin(admin.ModelAdmin):
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'organisation', 'position')
    list_filter = ('name', 'organisation')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'organisation', 'answers_type')
    list_filter = ('text', 'organisation', 'answers_type')
    search_fields = ('text', 'organisation')


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Presentation, PresentationAdmin)
admin.site.register(ProjectUser)
admin.site.register(CoreSlide)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(UserAnswer)
