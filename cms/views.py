#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import ContextMixin, View
from presentations.models import Organisation, Question, Answer, Presentation
from django.core.urlresolvers import reverse


class BaseQuestionView(ContextMixin, View):

    def __init__(self):
        self.model = Question
        self.pk_url_kwarg = 'question'
        self.tab = 'tab_questions'

    def get_context_data(self, **kwargs):
        context = super(BaseQuestionView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        return context

    # ?не наследуется

    # def get_success_url(self):
    #     return reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})


class BasePresentationsView(ContextMixin, View):

    def __init__(self):
        self.model = Presentation
        self.pk_url_kwarg = 'presentation'
        self.tab = 'tab_presentations'

    def get_context_data(self, **kwargs):
        context = super(BasePresentationsView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        return context


class BaseAnswerView(ContextMixin, View):

    def __init__(self):
        self.model = Answer
        self.pk_url_kwarg = 'answer'
        self.tab = 'tab_questions'

    def get_context_data(self, **kwargs):
        context = super(BaseAnswerView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        if 'question' in self.kwargs:
            context['question'] = \
                Question.objects.get(pk=self.kwargs['question'])
            context['answers_list'] = \
                Answer.objects.filter(question=self.kwargs['question'])
        return context

    def get_success_url(self):
        return reverse('cms:questions-detail', kwargs={'organisation': self.kwargs['organisation'],
                                                       'question': self.kwargs['question']})


class BackBtnToListQuestion(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(BackBtnToListQuestion, self).get_context_data(**kwargs)
        context['back_button'] = reverse('cms:questions-list', kwargs={'organisation': self.kwargs['organisation']})
        return context


class BackBtnToQuestion(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(BackBtnToQuestion, self).get_context_data(**kwargs)
        context['back_button'] = reverse('cms:questions-detail', kwargs={'organisation': self.kwargs['organisation'],
                                         'question': self.kwargs['question']})
        return context


class QuestionAddBtn(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(QuestionAddBtn, self).get_context_data(**kwargs)
        context['add_button'] = reverse('cms:questions-add', kwargs={'organisation': self.kwargs['organisation']})
        return context


class QuestionEditBtn(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(QuestionEditBtn, self).get_context_data(**kwargs)
        context['edit_button'] = reverse('cms:questions-edit', kwargs={'organisation': self.kwargs['organisation'],
                                         'question': self.kwargs['question']})
        return context


class QuestionDelBtn(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(QuestionDelBtn, self).get_context_data(**kwargs)
        context['del_button'] = reverse('cms:questions-delete', kwargs={'organisation': self.kwargs['organisation'],
                                        'question': self.kwargs['question']})
        return context


class AnswerAddBtn(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(AnswerAddBtn, self).get_context_data(**kwargs)
        context['add_button'] = reverse('cms:answers-add', kwargs={'organisation': self.kwargs['organisation'],
                                        'question': self.kwargs['question']})
        return context


class AnswerDelBtn(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(AnswerDelBtn, self).get_context_data(**kwargs)
        context['del_button'] = reverse('cms:answers-delete', kwargs={'organisation': self.kwargs['organisation'],
                                        'question': self.kwargs['question'], 'answer': self.kwargs['answer']})
        return context


class BackBtnToListPresentation(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(BackBtnToListPresentation, self).get_context_data(**kwargs)
        context['back_button'] = reverse('cms:presentations-list', kwargs={'organisation': self.kwargs['organisation']})
        return context


class PresentationAddBtn(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(PresentationAddBtn, self).get_context_data(**kwargs)
        context['add_button'] = reverse('cms:presentations-add', kwargs={'organisation': self.kwargs['organisation']})
        return context
