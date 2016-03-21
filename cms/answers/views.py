#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from presentations.models import Question, Answer
from django.views.generic import CreateView, DeleteView, UpdateView
from cms.answers.forms import AnswerForm
from cms.views import BaseAnswerView
from cms.views import BackBtnToQuestion, AnswerDelBtn
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


class AnswerCreateView(BaseAnswerView, CreateView, BackBtnToQuestion):
    form_class = AnswerForm
    template_name = "cms/answers/edit.html"
    title = 'Добавление ответа'
    mode = 'Создать'

    def get_initial(self):
        initial = super(AnswerCreateView, self).get_initial()
        initial_new = initial.copy()
        initial_new['question'] = Question.objects.get(id=self.kwargs['question'])
        return initial_new


class AnswerUpdateView(BaseAnswerView, UpdateView, BackBtnToQuestion, AnswerDelBtn):
    form_class = AnswerForm
    template_name = "cms/answers/edit.html"
    title = 'Редактирование ответа'
    mode = 'Обновить'


class AnswerDeleteView(BaseAnswerView, DeleteView):
    pass


@login_required
@require_POST
def answer_up(request, **kwargs):
    answer = Answer.objects.get(id=kwargs['answer'])
    previous = answer.get_previous
    if previous:
        previous.position += 1
        answer.position -= 1
        previous.save()
        answer.save()
    return HttpResponseRedirect(reverse('cms:questions-detail', args=[kwargs['organisation'], kwargs['question']]))


@login_required
@require_POST
def answer_down(request, **kwargs):
    answer = Answer.objects.get(id=kwargs['answer'])
    next = answer.get_next
    if next:
        next.position -= 1
        answer.position += 1
        next.save()
        answer.save()
    return HttpResponseRedirect(reverse('cms:questions-detail', args=[kwargs['organisation'], kwargs['question']]))