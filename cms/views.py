#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import ContextMixin, View
from presentations.models import Organisation, Question, Answer, Presentation, CoreSlide
from django.core.urlresolvers import reverse


class FillContextMixin(ContextMixin, View):
    # TODO ты все внес в один миксин, по хорошему все относящееся к вопросам - в базовый для вопросов и т.д.
    has_back_to_question_list = False
    has_question_add_btn = False
    has_question_edit_btn = False
    has_question_delete_btn = False

    has_back_to_question = False
    has_answer_add_btn = False
    has_answer_edit_btn = False
    has_answer_delete_btn = False

    has_back_to_presentation_list = False
    has_presentation_add_btn = False
    has_presentation_edit_btn = False
    has_presentation_delete_btn = False

    has_back_to_presentation = False
    has_slide_add_btn = False
    has_slide_edit_btn = False
    has_slide_delete_btn = False

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

        url_kwargs = {'organisation': self.kwargs['organisation']}

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

        if 'presentation' in self.kwargs:
            kwargs_presentation = {'organisation': self.kwargs['organisation'],
                                   'presentation': self.kwargs['presentation']}
        else:
            kwargs_presentation = None

        if 'slide' in self.kwargs:
            kwargs_slide = {'organisation': self.kwargs['organisation'],
                            'presentation': self.kwargs['presentation'],
                            'slide': self.kwargs['slide']}
        else:
            kwargs_slide = None

        if self.has_back_to_question_list:
            context['back_button'] = reverse('cms:questions_list', kwargs=url_kwargs)
        if self.has_question_add_btn:
            context['add_button'] = reverse('cms:questions_add', kwargs=url_kwargs)
        if self.has_question_edit_btn:
            context['edit_button'] = reverse('cms:questions_edit', kwargs=kwargs_question)
        if self.has_question_delete_btn:
            context['del_button'] = reverse('cms:questions_delete', kwargs=kwargs_question)

        if self.has_back_to_question:
            context['back_button'] = reverse('cms:questions_detail', kwargs=kwargs_question)
        if self.has_answer_add_btn:
            context['add_button'] = reverse('cms:answers_add', kwargs=kwargs_question)
        if self.has_answer_edit_btn:
            context['edit_button'] = reverse('cms:answers_edit', kwargs=kwargs_answer)
        if self.has_answer_delete_btn:
            context['del_button'] = reverse('cms:answers_delete', kwargs=kwargs_answer)

        if self.has_back_to_presentation_list:
            context['back_button'] = reverse('cms:presentations_list', kwargs=url_kwargs)
        if self.has_presentation_add_btn:
            context['add_button'] = reverse('cms:presentations_add', kwargs=url_kwargs)
        if self.has_presentation_edit_btn:
            context['edit_button'] = reverse('cms:presentations_edit', kwargs=kwargs_presentation)
        if self.has_presentation_delete_btn:
            context['del_button'] = reverse('cms:presentations_delete', kwargs=kwargs_presentation)

        if self.has_back_to_presentation:
            context['back_button'] = reverse('cms:presentations_detail', kwargs=kwargs_presentation)
        if self.has_slide_add_btn:
            context['add_button'] = reverse('cms:slides_add', kwargs=kwargs_presentation)
        if self.has_slide_edit_btn:
            context['edit_button'] = reverse('cms:slides_edit', kwargs=kwargs_slide)
        if self.has_slide_delete_btn:
            context['del_button'] = reverse('cms:slides_delete', kwargs=kwargs_slide)

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
        return reverse('cms:questions_detail', kwargs={'organisation': self.kwargs['organisation'],
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
        return reverse('cms:presentations_detail', kwargs={'organisation': self.kwargs['organisation'],
                                                           'presentation': self.kwargs['presentation']})
