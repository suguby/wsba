# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import CharField, IntegerField, TextField


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
    presentation_number = IntegerField(verbose_name='Номер презентации') # Ссылка на номер обучающей презентации
    question_number = IntegerField(verbose_name='Номер вопроса')
    question_text = TextField(verbose_name='Текст вопроса')
    answer_type = IntegerField(verbose_name='Тип ответа') # Номер типа вопроса (0 - да/нет; 1 - список; 2 - список с комментарием)
    # TODO Создать модель Типы ответов
    right_answer = IntegerField(verbose_name='Правильный ответ') # Номер правильного ответа

    class Meta:
        db_table = 'questions'

class AnswerVariants(models.Model):
    question = models.ForeignKey(Questions)
    answer_number = IntegerField(verbose_name='Номер ответа') # Порядковый номер ответа
    answer_text = CharField(verbose_name='Текст ответа', max_length=64)

    class Meta:
        db_table = 'answer_variants'


class UserAnswers(models.Model):
    answer_variants = models.ForeignKey(AnswerVariants)
    user_id = IntegerField(verbose_name="Код пользователя")
    answer_number = IntegerField(verbose_name='Номер ответа')
    answer_comment = TextField(verbose_name='Комментарий') # используется только при Типе вопроса "Список с комментарием"
    # может быть лучше вынести в отдельную модель

