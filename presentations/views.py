# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import DetailView, TemplateView

from presentations.models import Question, Answer, CoreSlide


class SlideView(TemplateView):
    model = Question

    def get_context_data(self, **kwargs):

        # question = Question.objects.get(presentation_number_id__exact=self.args[1], number__exact=self.args[2])
        for slide in CoreSlide.objects.filter(id=kwargs['slide']).select_related('question'):
            question = slide.question
            break
        else:
            raise Exception('Нет такого слайда!!!')

        self.answer_type = question.answers_type

        context = super(SlideView, self).get_context_data(**kwargs)
        context['variants'] = Answer.objects.filter(question_id=question.id)
        # TODO не надо переназывать сущности в шаблоне - если это Answer то и назови answers
        context['question_text'] = question.text
        # а можно в шаблон передать аттрибут класса? question.text например
        # TODO можно конечно. лучше просто передавать обьект, а в шаблоне использовать {{ question.text }}
        if self.answer_type == 'YN':
            self.template_name = 'presentations/yes_no_question.html'
        elif self.answer_type == 'L':
            self.template_name = 'presentations/list_question.html'
        elif self.answer_type == 'LC':
            self.template_name = 'presentations/list_and_comment_question.html'
        # TODO все шаблоны практически одинаковы - копипаста с небольшими изменениями :(
        # надо унифицировать - передавать тип вопроса, и от него делать или radio или choice
        # так же и с вариантами ответа - если variant.has_comment - то показывать input text


        return context

