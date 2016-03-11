#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from presentations.models import Question, Organisation, Answer
from django.views.generic import ListView, DetailView, CreateView
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
        return Question.objects.all()


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'cms/questions/detail.html'
    title = 'Вопрос'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        context['answers_list'] = Answer.objects.filter(question=self.kwargs['pk'])

        return context


class QuestionCreateView(CreateView):
    form_class = QuestionForm
    template_name = "cms/questions/create.html"
    title = 'Добавление вопроса'

    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        return context

    def get_success_url(self):
        if 'organisation' in self.kwargs:
            return reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})
