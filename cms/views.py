#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import ContextMixin, View
from presentations.models import Organisation, Question, Answer, Presentation, CoreSlide
from django.core.urlresolvers import reverse


class FillContextMixin(ContextMixin, View):

    has_back_to_question_list = False
    has_question_add_btn = False
    has_question_edit_btn = False
    has_question_delete_btn = False

    has_back_to_question = False
    has_answer_add_btn = False
    has_answer_edit_btn = False
    has_answer_delete_btn = False

    def get_context_data(self, **kwargs):
        context = super(FillContextMixin, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        if 'question' in self.kwargs:
            context['question'] = \
                Question.objects.get(pk=self.kwargs['question'])
            context['answers_list'] = \
                Answer.objects.filter(question=self.kwargs['question'])
        if 'presentation' in self.kwargs:
            context['presentation'] = \
                Presentation.objects.get(pk=self.kwargs['presentation'])
            context['slide_list'] = \
                CoreSlide.objects.filter(presentation=self.kwargs['presentation'])

        kwargs = {'organisation': self.kwargs['organisation']}

        if 'question' in self.kwargs:
            kwargs_question = {'organisation': self.kwargs['organisation'],
                               'question': self.kwargs['question']}
        else:
            kwargs_question = None

        if 'answer' in self.kwargs:
            kwargs_answer = {'organisation': self.kwargs['organisation'],
                             'question': self.kwargs['question'],
                             'answer': self.kwargs['answer']}
        else:
            kwargs_answer = None

        if self.has_back_to_question_list:
            context['back_button'] = reverse('cms:questions-list', kwargs=kwargs)
        if self.has_question_add_btn:
            context['add_button'] = reverse('cms:questions-add', kwargs=kwargs)
        if self.has_question_edit_btn:
            context['edit_button'] = reverse('cms:questions-edit', kwargs=kwargs_question)
        if self.has_question_delete_btn:
            context['del_button'] = reverse('cms:questions-delete', kwargs=kwargs_question)
        if self.has_back_to_question:
            context['back_button'] = reverse('cms:questions-detail', kwargs=kwargs_question)
        if self.has_answer_add_btn:
            context['add_button'] = reverse('cms:answers-add', kwargs=kwargs_question)
        if self.has_answer_edit_btn:
            context['edit_button'] = reverse('cms:answers-edit', kwargs=kwargs_answer)
        if self.has_answer_delete_btn:
            context['del_button'] = reverse('cms:answers-delete', kwargs=kwargs_answer)
        return context


class BaseQuestionView(FillContextMixin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Question
        self.pk_url_kwarg = 'question'
        self.tab = 'tab_questions'


class BaseAnswerView(FillContextMixin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Answer
        self.pk_url_kwarg = 'answer'
        self.tab = 'tab_questions'

    def get_success_url(self):
        return reverse('cms:questions-detail', kwargs={'organisation': self.kwargs['organisation'],
                                                       'question': self.kwargs['question']})


class BasePresentationsView(FillContextMixin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Presentation
        self.pk_url_kwarg = 'presentation'
        self.tab = 'tab_presentations'


class BaseSlideView(FillContextMixin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = CoreSlide
        self.pk_url_kwarg = 'slide'
        self.tab = 'tab_presentations'

    def get_success_url(self):
        return reverse('cms:presentations-detail', kwargs={'organisation': self.kwargs['organisation'],
                                                           'presentation': self.kwargs['presentation']})


class BackBtnToListPresentation(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(BackBtnToListPresentation, self).get_context_data(**kwargs)
        context['back_button'] = reverse('cms:presentations-list', kwargs={'organisation': self.kwargs['organisation']})
        return context


class BackBtnToPresentation(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(BackBtnToPresentation, self).get_context_data(**kwargs)
        context['back_button'] = reverse('cms:presentations-detail', kwargs={'organisation': self.kwargs['organisation'],
                                         'presentation': self.kwargs['presentation']})
        return context


class PresentationAddBtn(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(PresentationAddBtn, self).get_context_data(**kwargs)
        context['add_button'] = reverse('cms:presentations-add', kwargs={'organisation': self.kwargs['organisation']})
        return context


class PresentationEditBtn(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(PresentationEditBtn, self).get_context_data(**kwargs)
        context['edit_button'] = reverse('cms:presentations-edit', kwargs={'organisation': self.kwargs['organisation'],
                                         'presentation': self.kwargs['presentation']})
        return context


class PresentationDelBtn(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(PresentationDelBtn, self).get_context_data(**kwargs)
        context['del_button'] = reverse('cms:presentations-delete', kwargs={'organisation': self.kwargs['organisation'],
                                        'presentation': self.kwargs['presentation']})
        return context


class SlideAddBtn(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(SlideAddBtn, self).get_context_data(**kwargs)
        context['add_button'] = reverse('cms:slides-add', kwargs={'organisation': self.kwargs['organisation'],
                                        'presentation': self.kwargs['presentation']})
        return context


class SlideDelBtn(ContextMixin, View):

    def get_context_data(self, **kwargs):
        context = super(SlideDelBtn, self).get_context_data(**kwargs)
        context['del_button'] = reverse('cms:slides-delete', kwargs={'organisation': self.kwargs['organisation'],
                                        'presentation': self.kwargs['presentation'], 'slide': self.kwargs['slide']})
        return context
