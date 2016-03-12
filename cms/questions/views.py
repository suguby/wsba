#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from presentations.models import Question, Organisation, Answer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from cms.questions.forms import QuestionForm


class QuestionListView(ListView):
    model = Question
    template_name = 'cms/questions/list.html'
    tab = 'question'
    title = 'Вопросы'

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        return context

    def get_queryset(self):
        org = self.kwargs['organisation']
        return Question.objects.all().order_by('number')


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'cms/questions/detail.html'
    title = 'Вопрос'
    pk_url_kwarg = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        context['answers_list'] = Answer.objects.filter(question=self.kwargs['question'])
        return context


class QuestionCreateView(CreateView):
    form_class = QuestionForm
    template_name = "cms/questions/edit.html"
    title = 'Добавление вопроса'
    mode = 'Создать'
    pk_url_kwarg = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        return context

    def get_success_url(self):
        if 'organisation' in self.kwargs:
            return reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})


class QuestionUpdateView(UpdateView):
    model = Question
    template_name = "cms/questions/edit.html"
    fields = ['number', 'text', 'answers_type']
    title = 'Редактирование вопроса'
    mode = 'Обновить'
    pk_url_kwarg = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        return context

    def get_success_url(self):
        # TODO: редирект на разные страницы
        if 'organisation' in self.kwargs:
            return reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})


class QuestionDeleteView(DeleteView):
    model = Question
    pk_url_kwarg = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDeleteView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        return context

    def get_success_url(self):
        if 'organisation' in self.kwargs:
            return reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})
