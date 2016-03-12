#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from presentations.models import Question, Organisation, Answer
from django.views.generic import CreateView, DeleteView
from cms.answers.forms import AnswerForm


class AnswerCreateView(CreateView):
    form_class = AnswerForm
    template_name = "cms/answers/edit.html"
    title = 'Добавление ответа'
    mode = 'Создать'
    pk_url_kwarg = 'answer'

    def get_initial(self):
        initial = super(AnswerCreateView, self).get_initial()
        initial_new = initial.copy()
        initial_new['question'] = Question.objects.get(id=self.kwargs['question'])
        return initial_new

    def get_context_data(self, **kwargs):
        context = super(AnswerCreateView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        if 'question' in self.kwargs:
            context['question'] = \
                Question.objects.get(pk=self.kwargs['question'])
            context['answers_list'] = Answer.objects.filter(question=self.kwargs['question']).order_by('variant_number')
        return context

    def get_success_url(self):
        return reverse('cms:questions-detail', kwargs={'organisation': self.kwargs['organisation'],
                                                       'question': self.kwargs['question']})


class AnswerDeleteView(DeleteView):
    model = Answer
    pk_url_kwarg = 'answer'

    def get_context_data(self, **kwargs):
        context = super(AnswerDeleteView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        if 'question' in self.kwargs:
            context['question'] = \
                Question.objects.get(pk=self.kwargs['question'])
            context['answers_list'] = Answer.objects.filter(question=self.kwargs['question']).order_by('variant_number')
        return context

    def get_success_url(self):
        return reverse('cms:questions-detail', kwargs={'organisation': self.kwargs['organisation'],
                                                       'question': self.kwargs['question']})
