# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.

from .models import Organisation, Presentation, ProjectUser, CoreSlide, Question, Answer, UserAnswer


class SlugNameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Organisation, SlugNameAdmin)

admin.site.register(Presentation)
admin.site.register(ProjectUser)
admin.site.register(CoreSlide)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserAnswer)
