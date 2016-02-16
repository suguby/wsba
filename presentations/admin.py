# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.

from .models import Organisation, Presentation, ProjectUser, CoreSlide, Question, Answer, UserAnswer


admin.site.register(Organisation)
admin.site.register(Presentation)
admin.site.register(ProjectUser)
admin.site.register(CoreSlide)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserAnswer)
