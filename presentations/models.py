# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import CharField, IntegerField, TextField

from user_interface.models import ProjectUser


class Organisation(models.Model):
    name = models.CharField(verbose_name='Название организации', max_length=64)
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)

    class Meta:
        db_table = 'organisations'


class Presentation(models.Model):
    organisation = models.ForeignKey(Organisation)
    name = models.CharField(verbose_name='Название презентации', max_length=64)
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True)
    position = models.IntegerField(verbose_name='Позиция', default=0)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)

    class Meta:
        db_table = 'presentations'


class CoreSlide(models.Model):
    presentation = models.ForeignKey(Presentation)
    image = models.ImageField()
    description = models.TextField()
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True)
    position = models.IntegerField(verbose_name='Позиция', default=0)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)

    class Meta:
        db_table = 'slides'


class Questions(models.Model):
    presentation_number = models.ForeignKey(Presentation, verbose_name='Номер презентации')
    number = IntegerField(verbose_name='Номер вопроса')
    text = TextField(verbose_name='Текст вопроса')
    answer_type = IntegerField(verbose_name='Тип ответа')
    # TODO просто будем наследовать модели от этой
    right_answer = models.BooleanField(verbose_name='Является правильным ответом')

    class Meta:
        db_table = 'questions'


class Answers(models.Model):
    question = models.ForeignKey(Questions)
    text = CharField(verbose_name='Текст ответа', max_length=64)

    class Meta:
        db_table = 'answers'


class UserAnswers(models.Model):
    """
        наличие этой записи соответствует ответу user на вариант answer
        иногда может быть комментарий к ответу
    """
    user = models.ForeignKey(ProjectUser, verbose_name="Пользователь")
    answer = models.ForeignKey(Answers, verbose_name="Ответ")
    comment = TextField(verbose_name='Комментарий', blank=True, null=True)

    class Meta:
        db_table = 'user_answers'
