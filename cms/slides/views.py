#!/usr/bin/env python
# -*- coding: utf-8 -*-

from presentations.models import Presentation
from django.views.generic import CreateView, DeleteView, UpdateView
from cms.slides.forms import SlideForm
from cms.views import BaseSlideView
from cms.views import BackBtnToPresentation, SlideDelBtn


class SlideCreateView(BaseSlideView, CreateView, BackBtnToPresentation):
    form_class = SlideForm
    template_name = "cms/slides/edit.html"
    title = 'Добавление слайда'
    mode = 'Создать'

    def get_initial(self):
        initial = super(SlideCreateView, self).get_initial()
        initial_new = initial.copy()
        initial_new['presentation'] = Presentation.objects.get(id=self.kwargs['presentation'])
        return initial_new


class SlideUpdateView(BaseSlideView, UpdateView, BackBtnToPresentation, SlideDelBtn):
    form_class = SlideForm
    template_name = "cms/slides/edit.html"
    title = 'Редактирование слайда'
    mode = 'Обновить'


class SlideDeleteView(BaseSlideView, DeleteView):
    pass


