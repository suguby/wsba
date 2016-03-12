# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from presentations.models import CoreSlide, Organisation, Presentation, Question, Answer


class QuestionViewTests(TestCase):

    def setUp(self):
        organisation = Organisation.objects.create(name='Рога и Копыта')
        presentation = Presentation.objects.create(organisation=organisation)
        self.question = Question.objects.create(number=1, text='Кто виноват?', answers_type='single')
        self.slide = CoreSlide.objects.create(question=self.question, presentation=presentation)


    def test_no_question(self):
        self.question.delete()
        response = self.client.get(reverse('slide_view', kwargs={'slide': self.slide.id}))
        self.assertContains(response, '')

    def test_view(self):

        response = self.client.get(reverse('slide_view', kwargs={'slide': self.slide.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.text)

    def test_single_answer(self):
        answer1 = Answer.objects.create(question_id=self.question.id, variant_number=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, variant_number=1, text='No', has_comment=False)

        response = self.client.get(reverse('slide_view', kwargs={'slide': self.slide.id}))
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer1.id), haystack=response.rendered_content)
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer2.id), haystack=response.rendered_content)


