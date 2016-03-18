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
        verbose_name = 'Организация'
        verbose_name_plural = 'организации'

    def __str__(self):
        return self.name


class Presentation(models.Model):
    organisation = models.ForeignKey(Organisation)
    name = models.CharField(verbose_name='Название презентации', max_length=64)
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True)
    position = models.IntegerField(verbose_name='Позиция', default=0)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)

    class Meta:
        db_table = 'presentations'
        verbose_name = 'Презентация'
        verbose_name_plural = 'презентации'


class CoreSlide(models.Model):
    presentation = models.ForeignKey(Presentation, verbose_name='Презентация')
    question = models.ForeignKey('Question', null=True, blank=True)
    image = models.ImageField()
    description = models.TextField()
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True)
    position = models.IntegerField(verbose_name='Позиция', default=0)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True, null=True)
    modified_at = models.DateTimeField(verbose_name='Изменено', auto_now=True, null=True)

    class Meta:
        db_table = 'slides'
        verbose_name = 'Слайд'
        verbose_name_plural = 'слайды'


class Question(models.Model):
    ANSWER_TYPE = (
        # эти данные потом в БД хранить, и это могут быть миллионы дублей multi/single
        # это экономия на спичках - вопросов будет не миллион, а порядка 1000, пять лишних байт,
        # 1000 * 5 = 5000 байт ~ 5Кб ;) даже на миллионе ~ 5Мб...
        ('multi', 'Множественный выбор'),
        ('single', 'Единичный выбор'),
    )

    number = IntegerField(verbose_name='Номер вопроса')
    text = TextField(verbose_name='Текст вопроса')
    answers_type = CharField(verbose_name='Тип ответов', max_length=8, choices=ANSWER_TYPE, default='multi')
    organisation = models.ForeignKey(Organisation, null=True, blank=True)

    class Meta:
        db_table = 'questions'
        verbose_name = 'Вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question)
    variant_number = models.IntegerField(verbose_name='Номер варианта ответа')
    text = CharField(verbose_name='Текст ответа', max_length=64)
    is_right = models.BooleanField(verbose_name='Является правильным ответом')
    has_comment = models.BooleanField(verbose_name="Ответ с комментарием")

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'answers'
        verbose_name = 'Ответ'
        verbose_name_plural = 'ответы'


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
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'ответы пользователей'
