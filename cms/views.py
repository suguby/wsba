#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import ContextMixin, View
from presentations.models import Organisation, Question, Answer, Presentation, CoreSlide
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


class BaseSlideView(ContextMixin, View):

    def __init__(self):
        self.model = CoreSlide
        self.pk_url_kwarg = 'slide'
        self.tab = 'tab_presentation'

    def get_context_data(self, **kwargs):
        context = super(BaseSlideView, self).get_context_data(**kwargs)
        if 'organisation' in self.kwargs:
            context['organisation'] = \
                Organisation.objects.get(slug=self.kwargs['organisation'])
        if 'presentation' in self.kwargs:
            context['presentation'] = \
                Presentation.objects.get(pk=self.kwargs['presentation'])
            context['slide_list'] = \
                CoreSlide.objects.filter(presentation=self.kwargs['presentation'])
        return context

    def get_success_url(self):
        return reverse('cms:presentations-detail', kwargs={'organisation': self.kwargs['organisation'],
                                                           'presentation': self.kwargs['presentation']})


# TODO не нравится что много копипасты - меняются только названия параметров
# может сделать так
class FillContextMixin(ContextMixin, View):
    has_back_to_question_list = False
    has_question_add_btn = False

    def get_context_data(self, **kwargs):
        context = super(FillContextMixin, self).get_context_data(**kwargs)
        kwargs = {'organisation': self.kwargs['organisation']}
        if self.has_back_to_question_list:
            context['back_button'] = reverse('cms:questions-list', kwargs=kwargs)
        if self.has_question_add_btn:
            context['add_button'] = reverse('cms:questions-add', kwargs=kwargs)
# тогда будет одно место, где мы заполняем контекст нужными значениями
# а тесты помогут сохранить целостность при рефакторе :)


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
