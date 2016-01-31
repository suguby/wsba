# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import DetailView, TemplateView

from presentations.models import Question, Answer


class CoreSlide(DetailView):
    pass


class SlideView(TemplateView):
    model = Question

    def get_context_data(self, **kwargs):
        question = Question.objects.get(presentation_number_id__exact=self.args[1], number__exact=self.args[2])
        self.answer_type = question.answers_type

        context = super(SlideView, self).get_context_data(**kwargs)
        context['variants'] = Answer.objects.filter(question_id=question.id)
        context['question_text'] = question.text # а можно в шаблон передать аттрибут класса? question.text например
        if self.answer_type == 'YN':
            self.template_name = 'presentations/yes_no_question.html'
        elif self.answer_type == 'L':
            self.template_name = 'presentations/list_question.html'
        elif self.answer_type == 'LC':
            self.template_name = 'presentations/list_and_comment_question.html'

        return context

