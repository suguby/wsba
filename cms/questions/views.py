#!/usr/bin/env python
# -*- coding: utf-8 -*-

from presentations.models import Question, Organisation, Answer
from django.views.generic import ListView, DetailView


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
        return Question.objects.filter()


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
