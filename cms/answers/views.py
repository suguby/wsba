#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from presentations.models import Question, Organisation, Answer
from django.views.generic import CreateView
from cms.answers.forms import AnswerForm


class AnswerCreateView(CreateView):
    form_class = AnswerForm
    template_name = "cms/answers/edit.html"
    title = 'Добавление ответа'
    mode = 'Создать'

    def get_initial(self):
        initial = super(AnswerCreateView, self).get_initial()
        initial_new = initial.copy()
        question = Question.objects.get(id=self.kwargs['pk'])
        initial_new['question'] = question
        return initial_new

    def get_form(self, form_class=None):
        form = super(AnswerCreateView, self).get_form()
        form.fields['question'].visible = False
        return form

    def get_context_data(self, **kwargs):
        context = super(AnswerCreateView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        if 'pk' in self.kwargs:
            context['question'] = \
                Question.objects.get(pk=self.kwargs['pk'])
            context['answers_list'] = Answer.objects.filter(question=self.kwargs['pk'])
        return context

    def get_success_url(self):
        if 'organisation' in self.kwargs:
            return reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})
