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
    presentation_number = models.ForeignKey(Presentation, verbose_name='Презентация')
    # TODO здесь суффикс _number не нужен - думай о поле как о ссылке на презентацию
    question = models.ForeignKey(Question, null=True, blank=True)
    image = models.ImageField()
    description = models.TextField()
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True)
    position = models.IntegerField(verbose_name='Позиция', default=0)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)

    class Meta:
        db_table = 'slides'


class Question(models.Model):
    number = IntegerField(verbose_name='Номер вопроса')
    text = TextField(verbose_name='Текст вопроса')
    ANSWER_TYPE = (
        ('YN', 'Yes_or_NO'),
        ('L', 'List'),
        ('LC', 'List_and_comment'),
    )  # Изучи model_utils.Choices  http://django-model-utils.readthedocs.org/en/latest/utilities.html#choices
    answers_type = CharField(verbose_name='Тип ответов', max_length=2, choices=ANSWER_TYPE)

    class Meta:
        db_table = 'questions'


class Answer(models.Model):
    question = models.ForeignKey(Question)
    variant_number = models.IntegerField(verbose_name='Номер варианта ответа')
    text = CharField(verbose_name='Текст ответа', max_length=64)
    is_right = models.BooleanField(verbose_name='Является правильным ответом')

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'answers'


class UserAnswer(models.Model):
    """
        наличие этой записи соответствует ответу user на вариант answer
        иногда может быть комментарий к ответу
    """
    user = models.ForeignKey(ProjectUser, verbose_name="Пользователь")
    answer = models.ForeignKey(Answer, verbose_name="Ответ")
    comment = TextField(verbose_name='Комментарий', blank=True, null=True)

    class Meta:
        db_table = 'user_answers'
