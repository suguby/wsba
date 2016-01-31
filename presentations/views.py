# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import DetailView

from presentations.models import Question, Answer


class CoreSlide(DetailView):
    pass


class SlideView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(SlideView, self).get_context_data(**kwargs)

        self.answer_type = Question.objects.get(presentation_number_id=self.args[1], number=self.args[2])
        self.text = get_object_or_404(Question,)
        Question.objects.filter(publisher=self.answer_type)

        if self.answer_type == 'YN':
            self.template_name = 'presentations/yes_no_question.html'
        elif self.answer_type == 'L':
            self.template_name = 'presentations/list_question.html'
            context['answer_list'] = self.get_queryset()
        elif self.answer_type == 'LC':
            self.template_name = 'presentations/list_and_comment_question.html'
            context['answer_list'] = self.get_queryset()

        return context
