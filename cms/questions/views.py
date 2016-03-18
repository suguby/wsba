#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from presentations.models import Question, Answer, Organisation
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView
from cms.questions.forms import QuestionForm
from cms.views import BaseQuestionView
from cms.views import BackBtnToListQuestion, BackBtnToQuestion
from cms.views import QuestionEditBtn, QuestionAddBtn, QuestionDelBtn
from cms.views import AnswerAddBtn
from django.conf import settings
from django.db.models import Q


class QuestionListView(ListView, BaseQuestionView, QuestionAddBtn):
    """
    Представление для списка вопросов
    """
    template_name = 'cms/questions/list.html'
    tab = 'question'
    title = 'Вопросы'
    paginate_by = settings.PAGINATE

    def get_queryset(self):
        organisation = Organisation.objects.get(slug=self.kwargs['organisation']) or None
        return Question.objects.filter(Q(organisation=organisation)| Q(organisation=None)).order_by('number')

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['page_kwargs'] = {'organisation': self.kwargs['organisation']}
        return context


class QuestionDetailView(DetailView, BaseQuestionView, BackBtnToListQuestion,
                         QuestionEditBtn, QuestionDelBtn, AnswerAddBtn):
    """
    Представление для одного вопроса
    """
    template_name = 'cms/questions/detail.html'
    title = 'Вопрос'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answers_list'] = \
            Answer.objects.filter(question=self.kwargs['question']).order_by('variant_number')
        return context


class QuestionCreateView(FormView, BaseQuestionView, BackBtnToListQuestion):
    """
    Создание вопроса
    """
    form_class = QuestionForm
    template_name = "cms/questions/edit.html"
    title = 'Добавление вопроса'
    mode = 'Создать'

    def get_success_url(self):
        return reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})

    def form_valid(self, form):
        if not form.cleaned_data['common']:
            del form.cleaned_data['common']
            obj = Question.objects.create(**form.cleaned_data)
            obj.organisation = Organisation.objects.get(slug=self.kwargs['organisation'])
            obj.save()
        return super(QuestionCreateView, self).form_valid(form)


class QuestionUpdateView(UpdateView, BaseQuestionView, BackBtnToQuestion):
    """
    Изменение вопроса
    """
    form_class = QuestionForm
    template_name = "cms/questions/edit.html"
    title = 'Редактирование вопроса'
    mode = 'Обновить'

    def form_valid(self, form):
        if not form.cleaned_data['common']:
            del form.cleaned_data['common']
            obj = Question.objects.create(**form.cleaned_data)
            obj.organisation = Organisation.objects.get(slug=self.kwargs['organisation'])
            obj.save()
        return super(QuestionUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('cms:questions-detail', kwargs={'organisation': self.kwargs['organisation'],
                                                       'question': self.kwargs['question']})


class QuestionDeleteView(DeleteView, BaseQuestionView):
    """
    Удаление вопроса
    """
    def get_success_url(self):
        return reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})
