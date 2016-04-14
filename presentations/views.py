# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views.generic import TemplateView

from presentations.models import Answer, CoreSlide, UserAnswer


def _get_slide(kwargs):
    for slide in CoreSlide.objects.filter(id=kwargs['slide_id']).select_related('question'):
        break
    else:
        raise Exception('Нет такого слайда!!!')
    return slide


def slide_question_context(context, kwargs):
    slide = _get_slide(kwargs)
    # TODO отдавать только нужные ключи в контексте, внешний модуль будет делать update
    context['slide'] = slide
    if slide.question:
        user_saved_answers = UserAnswer.objects.filter(answer__question=slide.question, user_id=1)
        user_saved_answers = {a.answer_id: a for a in user_saved_answers}
        answers = Answer.objects.filter(question=slide.question)
        count = 0
        if len(user_saved_answers):
            for answer in answers:
                if answer.has_comment and answer.id in user_saved_answers:
                    answer.comment = user_saved_answers[answer.id].comment
                    count += 1
        context['answers'] = answers
        context['user_saved_answers'] = user_saved_answers


class SlideView(TemplateView):
    template_name = 'presentations/common_question.html'

    def get_context_data(self, **kwargs):
        context = super(SlideView, self).get_context_data(**kwargs)
        slide_question_context(context, kwargs)
        return context

    def post(self, request, *args, **kwargs):
        slide = _get_slide(kwargs)
        question = slide.question
        answers = Answer.objects.filter(question=question)
        user_old_answers = UserAnswer.objects.filter(answer__question=question, user_id=1)
        user_old_answers.delete()
        count = 0
        for answer in answers:
            if str(answer.id) in request.POST.getlist('group1'):
                if answer.has_comment:
                    comment = request.POST.getlist('comment')[count]
                    count += 1
                else:
                    comment = None
                us = UserAnswer(answer_id=answer.id, user_id=1, comment=comment)

                us.save()
        return redirect(request.POST.get('next', '/'))
