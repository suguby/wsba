#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from presentations.models import Question, Answer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from cms.questions.forms import QuestionForm
from cms.views import BaseQuestionView
from cms.views import BackBtnToListQuestion, BackBtnToQuestion
from cms.views import QuestionEditBtn, QuestionAddBtn, QuestionDelBtn
from cms.views import AnswerAddBtn


class QuestionListView(ListView, BaseQuestionView, QuestionAddBtn):
    model = Question
    template_name = 'cms/questions/list.html'
    tab = 'question'
    title = 'Вопросы'

    def get_queryset(self):
        return Question.objects.all().order_by('number')


class QuestionDetailView(DetailView, BaseQuestionView, BackBtnToListQuestion,
                         QuestionEditBtn, QuestionDelBtn, AnswerAddBtn):
    model = Question
    template_name = 'cms/questions/detail.html'
    title = 'Вопрос'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answers_list'] = \
            Answer.objects.filter(question=self.kwargs['question']).order_by('variant_number')
        return context


class QuestionCreateView(CreateView, BaseQuestionView, BackBtnToListQuestion):
    form_class = QuestionForm
    template_name = "cms/questions/edit.html"
    title = 'Добавление вопроса'
    mode = 'Создать'

    def get_success_url(self):
        if 'organisation' in self.kwargs:
            return reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})


class QuestionUpdateView(UpdateView, BaseQuestionView, BackBtnToQuestion):
    model = Question
    template_name = "cms/questions/edit.html"
    fields = ['number', 'text', 'answers_type']
    title = 'Редактирование вопроса'
    mode = 'Обновить'

    def get_success_url(self):
        # TODO: редирект на разные страницы
        if 'organisation' in self.kwargs:
            return reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})


class QuestionDeleteView(DeleteView, BaseQuestionView):
    model = Question

    def get_success_url(self):
        if 'organisation' in self.kwargs:
            return reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})
