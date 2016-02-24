# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView

from presentations.models import Question, Answer, CoreSlide, UserAnswer


class SlideView(TemplateView):
    template_name = 'presentations/common_question.html'

    def get_context_data(self, **kwargs):
        for slide in CoreSlide.objects.filter(id=kwargs['slide']):
            question = slide.question
            break
        else:
            raise Exception('Нет такого слайда!!!')

        context = super(SlideView, self).get_context_data(**kwargs)
        context['slide'] = slide
        context['answers'] = Answer.objects.filter(question_id=question.id)
        context['question'] = question

        return context

    def post(self, request, *args, **kwargs):
        for slide in CoreSlide.objects.filter(id=kwargs['slide']).select_related('question'):
            break
        else:
            raise Exception('Нет такого слайда!!!')
        question = slide.question
        answers = Answer.objects.filter(question=question)
        # TODO удалить все старые ответы при их наличии
            # todo 1) получить список id answers по id question
            # todo 2) удалить записи по списку id одним запросом
        for answer in answers:
            if str(answer.id) in request.POST.get('group1'):
                us = UserAnswer(answer_id=answer.id, user_id=1, comment=request.POST.get('comment'))
                us.save()
        return redirect(reverse('slide_view', kwargs=kwargs))


