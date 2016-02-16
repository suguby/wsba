# -*- coding: utf-8 -*-

from django.views.generic import DetailView, TemplateView

from presentations.models import Question, Answer, CoreSlide


class SlideView(TemplateView):
    model = Question  # TODO зачем здесь модель?
    template_name = 'presentations/common_question.html'

    def get_context_data(self, **kwargs):

        for slide in CoreSlide.objects.filter(id=kwargs['slide']).select_related('question'):
            question_number = slide.question.number
            break
        else:
            raise Exception('Нет такого слайда!!!')
        # TODO по идее question = slide.question не нужно еще один запрос делать
        question = Question.objects.get(number__exact=question_number)

        context = super(SlideView, self).get_context_data(**kwargs)
        context['slide'] = slide
        context['answers'] = Answer.objects.filter(question_id=question.id)
        # TODO не нужно делать трансляцию названий в контекст, просто передай туда question
        # и там бери question.text, question.answers_type, etc
        context['answers_type'] = question.answers_type
        context['question_text'] = question.text

        return context

    # TODO тут нужно сделать обработку формы - сохранять ответ пользователя на этот вопрос
    # TODO пользователь - с айдишником 1 (суперпользователь)

