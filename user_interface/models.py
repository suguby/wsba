# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class ProjectUser(User):
    organisation = models.ForeignKey('presentations.Organisation',
                                     related_name='organisation', null=True, blank=True)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        db_table = 'project_users'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserPresentation(models.Model):
    """
        связка пользователь - презентации..
        'когда кто какую проходил и сколько баллов набрал'
    """
    user = models.ForeignKey(ProjectUser)
    presentation = models.ForeignKey('presentations.Presentation')
    passage_time = models.TimeField(blank=True, null=True, verbose_name='Вреся прохождения')

    def __str__(self):
        return '{} - {}'.format(self.user, self.presentation)

    class Meta:
        db_table = 'user_presentations'
        verbose_name = "Завершенные презентации"
        verbose_name_plural = "Завершенные презентации"


class UserSlides(models.Model):
    """
        связка пользователь - слайд
        'что ответил на вопросы слайда'
    """
    user = models.ForeignKey(ProjectUser)
    slide = models.ForeignKey('presentations.CoreSlide')

    class Meta:
        db_table = 'user_slides'
