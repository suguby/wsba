#!/usr/bin/env python
# -*- coding: utf-8 -*-

from presentations.models import Presentation
from django.views.generic import CreateView, DeleteView, UpdateView
from cms.slides.forms import SlideForm
from cms.views import BaseSlideView
# from cms.views import BackBtnToPresentation, SlideDelBtn


class SlideCreateView(BaseSlideView, CreateView):
    form_class = SlideForm
    template_name = "cms/slides/edit.html"
    title = 'Добавление слайда'
    mode = 'Создать'
    has_back_to_presentation = True

    def get_initial(self):
        initial = super(SlideCreateView, self).get_initial()
        initial_new = initial.copy()
        initial_new['presentation'] = Presentation.objects.get(id=self.kwargs['presentation'])
        return initial_new


class SlideUpdateView(BaseSlideView, UpdateView):
    form_class = SlideForm
    template_name = "cms/slides/edit.html"
    title = 'Редактирование слайда'
    mode = 'Обновить'
    has_back_to_presentation = True
    has_slide_delete_btn = True


class SlideDeleteView(BaseSlideView, DeleteView):
    pass


