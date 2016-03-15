#!/usr/bin/env python
# -*- coding: utf-8 -*-
from presentations.models import Question, Answer
from django.views.generic import CreateView, DeleteView, UpdateView
from cms.answers.forms import AnswerForm
from cms.views import BaseAnswerView
from cms.views import BackBtnToQuestion, AnswerDelBtn


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
    model = Answer
    template_name = "cms/answers/edit.html"
    title = 'Редактирование ответа'
    mode = 'Обновить'


class AnswerDeleteView(BaseAnswerView, DeleteView):
    model = Answer
