# -*- coding: utf-8 -*-
from django.db import models


class ProjectUser(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'project_users'


class UserPresentation(models.Model):
    """
        связка пользователь - презентации
        'когда кто какую проходил и сколько баллов набрал'
    """
    user = models.ForeignKey(ProjectUser)
    presentation = models.ForeignKey('presentations.Presentation')

    class Meta:
        db_table = 'user_presentations'


class UserSlides(models.Model):
    """
        связка пользователь - слайд
        'что ответил на вопросы слайда'
    """
    user = models.ForeignKey(ProjectUser)
    slide = models.ForeignKey('presentations.CoreSlide')

    class Meta:
        db_table = 'user_slides'
