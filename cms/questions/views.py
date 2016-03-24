#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from presentations.models import Question, Organisation
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView
from cms.questions.forms import QuestionForm
from cms.views import BaseQuestionView
from django.conf import settings
from django.db.models import Q


class QuestionListView(ListView, BaseQuestionView):

    template_name = 'cms/questions/list.html'
    title = 'Вопросы'
    paginate_by = settings.PAGINATE
    has_question_add_btn = True

    def get_queryset(self):
        organisation = Organisation.objects.get(slug=self.kwargs['organisation']) or None
        return Question.objects.filter(Q(organisation=organisation) | Q(organisation=None))


class QuestionDetailView(DetailView, BaseQuestionView):

    template_name = 'cms/questions/detail.html'
    title = 'Вопрос'
    has_back_to_question_list = True
    has_question_edit_btn = True
    has_question_delete_btn = True
    has_answer_add_btn = True


class QuestionCreateView(FormView, BaseQuestionView):

    form_class = QuestionForm
    template_name = "cms/questions/edit.html"
    title = 'Добавление вопроса'
    mode = 'Создать'
    has_back_to_question_list = True

    def get_success_url(self):
        return reverse('cms:questions_list', kwargs={'organisation': self.kwargs['organisation']})

    def form_valid(self, form):
        if not form.cleaned_data['common']:
            del form.cleaned_data['common']
            obj = Question.objects.create(**form.cleaned_data)
            obj.organisation = Organisation.objects.get(slug=self.kwargs['organisation'])
            obj.save()
        return super(QuestionCreateView, self).form_valid(form)


class QuestionUpdateView(UpdateView, BaseQuestionView):

    form_class = QuestionForm
    template_name = "cms/questions/edit.html"
    title = 'Редактирование вопроса'
    mode = 'Обновить'
    has_back_to_question = True

    def form_valid(self, form):
        if not form.cleaned_data['common']:
            del form.cleaned_data['common']
            obj = Question.objects.create(**form.cleaned_data)
            obj.organisation = Organisation.objects.get(slug=self.kwargs['organisation'])
            obj.save()
        return super(QuestionUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('cms:questions_detail', kwargs={'organisation': self.kwargs['organisation'],
                                                       'question': self.kwargs['question']})


class QuestionDeleteView(DeleteView, BaseQuestionView):

    def get_success_url(self):
        return reverse('cms:questions_list', kwargs={'organisation': self.kwargs['organisation']})
