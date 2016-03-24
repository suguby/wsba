# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView

from presentations.models import Question, Answer, CoreSlide, UserAnswer


class SlideView(TemplateView):
    template_name = 'presentations/common_question.html'

    def get_context_data(self, **kwargs):
        for slide in CoreSlide.objects.filter(id=kwargs['slide']):
            break
        else:
            raise Exception('Нет такого слайда!!!')
        question = slide.question

        context = super(SlideView, self).get_context_data(**kwargs)
        context['slide'] = slide
        if question:
            user_saved_answers = UserAnswer.objects.filter(answer__question=question, user_id=1)
            user_saved_answers = {a.answer_id: a for a in user_saved_answers}
            answers = Answer.objects.filter(question=question)
            count = 0
            if len(user_saved_answers):
                for answer in answers:
                    if answer.has_comment:
                        answer.comment = user_saved_answers[answer.id].comment
                        count += 1
            context['answers'] = answers
            context['user_saved_answers'] = user_saved_answers
            context['question'] = question
        else:
            context['question'] = None
        return context

    def post(self, request, *args, **kwargs):
        for slide in CoreSlide.objects.filter(id=kwargs['slide']).select_related('question'):
            break
        else:
            raise Exception('Нет такого слайда!!!')
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
        return redirect(reverse('slide_view', kwargs=kwargs))


