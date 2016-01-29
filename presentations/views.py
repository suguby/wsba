# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from presentations.models import Question, Answer


class CoreSlide(DetailView):
    pass


class SlideView(CoreSlide):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(SlideView, self).get_context_data(**kwargs)
        # if answer_type == 'YN':
        #     context['answer_list'] = ['Да', 'Нет']
        context['answer_list'] = Answer.objects.all()

        return context
