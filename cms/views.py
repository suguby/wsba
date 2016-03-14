#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import ContextMixin, View
from presentations.models import Organisation, Question, Answer
from django.core.urlresolvers import reverse


class BaseQuestionView(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(BaseQuestionView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        return context


class BaseAnswerView(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(BaseAnswerView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        if 'question' in self.kwargs:
            context['question'] = \
                Question.objects.get(pk=self.kwargs['question'])
            context['answers_list'] = \
                Answer.objects.filter(question=self.kwargs['question']).order_by('variant_number')
        return context

    def get_success_url(self):
        return reverse('cms:questions-detail', kwargs={'organisation': self.kwargs['organisation'],
                                                       'question': self.kwargs['question']})
