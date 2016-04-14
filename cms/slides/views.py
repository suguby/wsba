#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from presentations.models import CoreSlide
from presentations.models import Presentation
from django.views.generic import CreateView, DeleteView, UpdateView
from cms.slides.forms import SlideForm
from cms.views import BaseSlideView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse


class SlideCreateView(LoginRequiredMixin, BaseSlideView, CreateView):
    form_class = SlideForm
    template_name = "cms/slides/edit.html"
    title = 'Добавление слайда'
    mode = 'Создать'
    has_back_to_presentation = True

    def get_initial(self):
        initial = super(SlideCreateView, self).get_initial()
        initial_new = initial.copy()
        initial_new['presentation'] = \
            Presentation.objects.get(id=self.kwargs['presentation'])
        return initial_new


class SlideUpdateView(LoginRequiredMixin, BaseSlideView, UpdateView):
    form_class = SlideForm
    template_name = "cms/slides/edit.html"
    title = 'Редактирование слайда'
    mode = 'Обновить'
    has_back_to_presentation = True
    has_slide_delete_btn = True


class SlideDeleteView(LoginRequiredMixin, BaseSlideView, DeleteView):
    pass


@login_required
@require_POST
def slide_up(request, **kwargs):
    slide = CoreSlide.objects.get(id=kwargs['slide'])
    previous_slide = slide.previous_slide
    if previous_slide:
        previous_slide.position += 1
        slide.position -= 1
        previous_slide.save()
        slide.save()
    return HttpResponseRedirect(reverse('cms:presentations_detail',
                                        args=[kwargs['organisation'],
                                              kwargs['presentation']]))


@login_required
@require_POST
def slide_down(request, **kwargs):
    slide = CoreSlide.objects.get(id=kwargs['slide'])
    next_slide = slide.next_slide
    if next_slide:
        next_slide.position -= 1
        slide.position += 1
        next_slide.save()
        slide.save()
    return HttpResponseRedirect(reverse('cms:presentations_detail',
                                        args=[kwargs['organisation'],
                                              kwargs['presentation']]))
