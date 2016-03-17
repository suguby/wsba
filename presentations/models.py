# -*- coding: utf-8 -*-

from django.db import models


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
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    class Meta:
        db_table = 'presentations'

    def __str__(self):
        return 'presentation: {name}, id: {id}'.format(name=self.name, id=self.id)


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
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"
