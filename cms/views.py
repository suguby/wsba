#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import ContextMixin, View
from presentations.models import Organisation, Question, Answer, \
    Presentation, CoreSlide
from django.core.urlresolvers import reverse


class BaseCmsWithContextView(ContextMixin, View):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
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
            context['slide_list'] = CoreSlide.objects.\
                filter(presentation=self.kwargs['presentation'])
        self.url_kwargs = {'organisation': self.kwargs['organisation']}

        if 'question' in self.kwargs:
            self.kwargs_question = \
                {'organisation': self.kwargs['organisation'],
                 'question': self.kwargs['question']}
        else:
            self.kwargs_question = None

        if 'presentation' in self.kwargs:
            self.kwargs_presentation = \
                {'organisation': self.kwargs['organisation'],
                 'presentation': self.kwargs['presentation']}
        else:
            self.kwargs_presentation = None

        return context


class BaseQuestionView(BaseCmsWithContextView):
    has_back_to_question_list = False
    has_question_add_btn = False
    has_question_edit_btn = False
    has_question_delete_btn = False
    has_answer_add_btn = False
    has_back_to_question = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Question
        self.pk_url_kwarg = 'question'
        self.tab = 'tab_questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.has_back_to_question_list:
            context['back_button'] = reverse('cms:questions_list',
                                             kwargs=self.url_kwargs)
        if self.has_question_add_btn:
            context['add_button'] = reverse('cms:questions_add',
                                            kwargs=self.url_kwargs)
        if self.has_question_edit_btn:
            context['edit_button'] = reverse('cms:questions_edit',
                                             kwargs=self.kwargs_question)
        if self.has_question_delete_btn:
            context['del_button'] = reverse('cms:questions_delete',
                                            kwargs=self.kwargs_question)
        if self.has_answer_add_btn:
            context['add_button'] = reverse('cms:answers_add',
                                            kwargs=self.kwargs_question)
        if self.has_back_to_question:
            context['back_button'] = reverse('cms:questions_detail',
                                             kwargs=self.kwargs_question)
        return context


class BaseAnswerView(BaseCmsWithContextView):
    has_back_to_question = False
    has_answer_delete_btn = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Answer
        self.pk_url_kwarg = 'answer'
        self.tab = 'tab_questions'

    def get_success_url(self):
        return reverse('cms:questions_detail',
                       kwargs={'organisation': self.kwargs['organisation'],
                               'question': self.kwargs['question']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'answer' in self.kwargs:
            kwargs_answer = {'organisation': self.kwargs['organisation'],
                             'question': self.kwargs['question'],
                             'answer': self.kwargs['answer']}
        else:
            kwargs_answer = None

        if self.has_back_to_question:
            context['back_button'] = reverse('cms:questions_detail',
                                             kwargs=self.kwargs_question)
        if self.has_answer_delete_btn:
            context['del_button'] = reverse('cms:answers_delete',
                                            kwargs=kwargs_answer)

        return context


class BasePresentationsView(BaseCmsWithContextView):
    has_presentation_add_btn = False
    has_back_to_presentation_list = False
    has_presentation_edit_btn = False
    has_presentation_delete_btn = False
    has_slide_add_btn = False
    has_back_to_presentation = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Presentation
        self.pk_url_kwarg = 'presentation'
        self.tab = 'tab_presentations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.has_back_to_presentation_list:
            context['back_button'] = reverse('cms:presentations_list',
                                             kwargs=self.url_kwargs)
        if self.has_presentation_add_btn:
            context['add_button'] = reverse('cms:presentations_add',
                                            kwargs=self.url_kwargs)
        if self.has_presentation_edit_btn:
            context['edit_button'] = reverse('cms:presentations_edit',
                                             kwargs=self.kwargs_presentation)
        if self.has_presentation_delete_btn:
            context['del_button'] = reverse('cms:presentations_delete',
                                            kwargs=self.kwargs_presentation)
        if self.has_back_to_presentation:
            context['back_button'] = reverse('cms:presentations_detail',
                                             kwargs=self.kwargs_presentation)
        if self.has_slide_add_btn:
            context['add_button'] = reverse('cms:slides_add',
                                            kwargs=self.kwargs_presentation)

        return context


class BaseSlideView(BaseCmsWithContextView):
    has_back_to_presentation = False
    has_slide_delete_btn = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = CoreSlide
        self.pk_url_kwarg = 'slide'
        self.tab = 'tab_presentations'

    def get_success_url(self):
        return reverse('cms:presentations_detail',
                       kwargs={'organisation': self.kwargs['organisation'],
                               'presentation': self.kwargs['presentation']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'slide' in self.kwargs:
            kwargs_slide = {'organisation': self.kwargs['organisation'],
                            'presentation': self.kwargs['presentation'],
                            'slide': self.kwargs['slide']}
        else:
            kwargs_slide = None

        if self.has_back_to_presentation:
            context['back_button'] = reverse('cms:presentations_detail',
                                             kwargs=self.kwargs_presentation)

        if self.has_slide_delete_btn:
            context['del_button'] = reverse('cms:slides_delete',
                                            kwargs=kwargs_slide)

        return context
