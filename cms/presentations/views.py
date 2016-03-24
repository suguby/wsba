#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from cms.views import BasePresentationsView
from presentations.models import Presentation, Organisation, CoreSlide
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.conf import settings
from .forms import PresentationForm


class PresentationListView(ListView, BasePresentationsView):

    template_name = 'cms/presentations/list.html'
    title = 'Презентации'
    paginate_by = settings.PAGINATE
    has_presentation_add_btn = True

    def get_queryset(self):
        organisation = Organisation.objects.get(slug=self.kwargs['organisation']) or None
        return Presentation.objects.filter(organisation=organisation).order_by('position')

    def get_context_data(self, **kwargs):
        context = super(PresentationListView, self).get_context_data(**kwargs)
        context['page_kwargs'] = {'organisation': self.kwargs['organisation']}
        return context


class PresentationDetailView(DetailView, BasePresentationsView):

    template_name = 'cms/presentations/detail.html'
    title = 'Презентация'
    has_back_to_presentation_list = True
    has_presentation_edit_btn = True
    has_presentation_delete_btn = True
    has_slide_add_btn = True

    def get_context_data(self, **kwargs):
        context = super(PresentationDetailView, self).get_context_data(**kwargs)
        context['slide_list'] = \
            CoreSlide.objects.filter(presentation=self.kwargs['presentation'])
        return context


class PresentationCreateView(CreateView, BasePresentationsView):

    form_class = PresentationForm
    template_name = "cms/presentations/edit.html"
    title = 'Добавление презентации'
    mode = 'Создать'
    has_back_to_presentation_list = True

    def get_initial(self):
        initial = super(PresentationCreateView, self).get_initial()
        initial_new = initial.copy()
        initial_new['organisation'] = Organisation.objects.get(slug=self.kwargs['organisation'])
        return initial_new

    def get_success_url(self):
        return reverse('cms:presentations_list', kwargs={'organisation': self.kwargs['organisation']})


class PresentationUpdateView(UpdateView, BasePresentationsView):

    form_class = PresentationForm
    template_name = "cms/presentations/edit.html"
    title = 'Редактирование презентации'
    mode = 'Обновить'
    has_back_to_presentation = True

    def get_success_url(self):
        return reverse('cms:presentations_detail', kwargs={'organisation': self.kwargs['organisation'],
                                                           'presentation': self.kwargs['presentation']})


class PresentationDeleteView(DeleteView, BasePresentationsView):

    def get_success_url(self):
        return reverse('cms:presentations_list', kwargs={'organisation': self.kwargs['organisation']})
