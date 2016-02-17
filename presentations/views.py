# -*- coding: utf-8 -*-

from django.views.generic import DetailView, TemplateView

from presentations.models import Question, Answer, CoreSlide


class SlideView(TemplateView):
    template_name = 'presentations/common_question.html'

    def get_context_data(self, **kwargs):

        for slide in CoreSlide.objects.filter(id=kwargs['slide']).select_related('question'):
            question_number = slide.question.number
            break
        else:
            raise Exception('Нет такого слайда!!!')
        # TODO по идее question = slide.question не нужно еще один запрос делать
        # может я что-то не понимаю, мне так кажется:
        # slide.question - это поле с номером, а question (тот что ниже) это запись из Question
        # TODO slide.question_id это поле с номером, а slide.question - собственно обьект
        question = Question.objects.get(number__exact=question_number)

        context = super(SlideView, self).get_context_data(**kwargs)
        context['slide'] = slide
        context['answers'] = Answer.objects.filter(question_id=question.id)
        context['question'] = question

        return context

    def post(self, request, *args, **kwargs):
        # TODO тут нужно сделать обработку формы - сохранять ответ пользователя на этот вопрос
        # TODO пользователь - с айдишником 1 (суперпользователь)
        for slide in CoreSlide.objects.filter(id=kwargs['slide']).select_related('question'):
            break
        else:
            raise Exception('Нет такого слайда!!!')
        question = slide.question
        for answer in Answer.objects.filter(question=question):
            # TODO проверяем все ответы на вопрос в request.POST и записываем в базу
            # TODO здесь поставь точку отладки - увидишь как джанга возвращает данные формы
            if answer.id in request.POST.get('group1'):
                pass


