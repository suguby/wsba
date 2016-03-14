#!/usr/bin/env python
# -*- coding: utf-8 -*-


from presentations.models import Question, Answer
from django.views.generic import CreateView, DeleteView, UpdateView
from cms.answers.forms import AnswerForm
from cms.views import BaseAnswerView


class AnswerCreateView(BaseAnswerView, CreateView):
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


class AnswerUpdateView(BaseAnswerView, UpdateView):
    form_class = AnswerForm
    model = Answer
    template_name = "cms/answers/edit.html"
    title = 'Редактирование ответа'
    mode = 'Обновить'
    pk_url_kwarg = 'answer'

    # def get_success_url(self):
    #     return reverse('cms:questions-detail', kwargs={'organisation': self.kwargs['organisation'],
    #                                                    'question': self.kwargs['question']})


class AnswerDeleteView(BaseAnswerView, DeleteView):
    model = Answer
    pk_url_kwarg = 'answer'
    #
    # def get_success_url(self):
    #     return reverse('cms:questions-detail', kwargs={'organisation': self.kwargs['organisation'],
    #                                                    'question': self.kwargs['question']})
