#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from cms.views import BasePresentationsView
from cms.views import PresentationAddBtn, BackBtnToListPresentation, BackBtnToPresentation, PresentationEditBtn, \
    PresentationDelBtn
from presentations.models import Presentation, Organisation, CoreSlide
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.conf import settings
from .forms import PresentationForm


class PresentationListView(ListView, BasePresentationsView, PresentationAddBtn):
    """
    Представление для списка презентаций
    """
    template_name = 'cms/presentations/list.html'
    title = 'Презентации'
    paginate_by = settings.PAGINATE

    def get_queryset(self):
        organisation = Organisation.objects.get(slug=self.kwargs['organisation']) or None
        return Presentation.objects.filter(organisation=organisation).order_by('position')

    def get_context_data(self, **kwargs):
        context = super(PresentationListView, self).get_context_data(**kwargs)
        context['page_kwargs'] = {'organisation': self.kwargs['organisation']}
        return context


class PresentationDetailView(DetailView, BasePresentationsView, BackBtnToListPresentation,
                             PresentationEditBtn, PresentationDelBtn):
    """
    Представление для презентации
    """
    template_name = 'cms/presentations/detail.html'
    title = 'Презентация'

    def get_context_data(self, **kwargs):
        context = super(PresentationDetailView, self).get_context_data(**kwargs)
        context['slide_list'] = \
            CoreSlide.objects.filter(presentation=self.kwargs['presentation'])
        return context


class PresentationCreateView(CreateView, BasePresentationsView, BackBtnToListPresentation):
    """
    Создание презентации
    """
    form_class = PresentationForm
    template_name = "cms/presentations/edit.html"
    title = 'Добавление презентации'
    mode = 'Создать'

    def get_initial(self):
        initial = super(PresentationCreateView, self).get_initial()
        initial_new = initial.copy()
        initial_new['organisation'] = Organisation.objects.get(slug=self.kwargs['organisation'])
        return initial_new

    def get_success_url(self):
        return reverse('cms:presentations-list', kwargs={'organisation': self.kwargs['organisation']})


class PresentationUpdateView(UpdateView, BasePresentationsView, BackBtnToPresentation):
    """
    Изменение презентации
    """
    form_class = PresentationForm
    template_name = "cms/presentations/edit.html"
    title = 'Редактирование вопроса'
    mode = 'Обновить'

    # def form_valid(self, form):
    #     if not form.cleaned_data['common']:
    #         del form.cleaned_data['common']
    #         obj = Question.objects.create(**form.cleaned_data)
    #         obj.organisation = Organisation.objects.get(slug=self.kwargs['organisation'])
    #         obj.save()
    #     return super(PresentationUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('cms:presentations-detail', kwargs={'organisation': self.kwargs['organisation'],
                                                           'presentation': self.kwargs['presentation']})


class PresentationDeleteView(DeleteView, BasePresentationsView):
    """
    Удаление презентации
    """
    def get_success_url(self):
        return reverse('cms:presentations-list', kwargs={'organisation': self.kwargs['organisation']})