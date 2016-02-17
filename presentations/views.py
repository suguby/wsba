# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import DetailView, TemplateView

from presentations.models import Question, Answer, CoreSlide


class SlideView(TemplateView):
    model = Question
    template_name = 'presentations/common_question.html'

    def get_context_data(self, **kwargs):

        for slide in CoreSlide.objects.filter(id=kwargs['slide']).select_related('question'):
            question_number = slide.question.number
            break
        else:
            raise Exception('Нет такого слайда!!!')
        question = Question.objects.get(number__exact=question_number)

        context = super(SlideView, self).get_context_data(**kwargs)
        context['slide'] = slide
        context['answers_type'] = question.answers_type
        context['answers'] = Answer.objects.filter(question_id=question.id)
        context['question_text'] = question.text

        return context

    def post(self, request, *args, **kwargs):
