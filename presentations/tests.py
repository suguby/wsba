# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from presentations.models import CoreSlide, Organisation, Presentation, Question, Answer


class QuestionViewTests(TestCase):

    def setUp(self):
        organisation = Organisation.objects.create(name='Рога и Копыта')
        self.presentation = Presentation.objects.create(organisation=organisation)


    def test_no_question(self):
        self.question = Question.objects.create(number=1, text='Кто виноват?', answers_type='single')
        self.slide = CoreSlide.objects.create(question=self.question, presentation=self.presentation)

        # self.slide.question = None
        response = self.client.get(reverse('slide_view', kwargs={'slide': self.slide.id}))
        self.assertInHTML(needle='<form method="post" action="">', haystack=response.rendered_content, count=0)

    def test_view(self):
        self.question = Question.objects.create(number=1, text='Кто виноват?', answers_type='single')
        self.slide = CoreSlide.objects.create(question=self.question, presentation=self.presentation)

        response = self.client.get(reverse('slide_view', kwargs={'slide': self.slide.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.text)

    def test_single_answer(self):
        self.question = Question.objects.create(number=1, text='Кто виноват?', answers_type='single')
        self.slide = CoreSlide.objects.create(question=self.question, presentation=self.presentation)

        answer1 = Answer.objects.create(question_id=self.question.id, variant_number=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, variant_number=2, text='No', has_comment=False)

        response = self.client.get(reverse('slide_view', kwargs={'slide': self.slide.id}))
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer1.id), haystack=response.rendered_content)
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer2.id), haystack=response.rendered_content)

    def test_single_comment_answer(self):
        self.question = Question.objects.create(number=1, text='Кто виноват?', answers_type='single')
        self.slide = CoreSlide.objects.create(question=self.question, presentation=self.presentation)

        answer1 = Answer.objects.create(question_id=self.question.id, variant_number=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, variant_number=2, text='No', has_comment=True)

        response = self.client.get(reverse('slide_view', kwargs={'slide': self.slide.id}))
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer1.id), haystack=response.rendered_content)
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer2.id), haystack=response.rendered_content)
        self.assertContains(response, "Комментарий:")

    def test_multi_answer(self):
        self.question = Question.objects.create(number=1, text='Кто виноват?', answers_type='multi')
        self.slide = CoreSlide.objects.create(question=self.question, presentation=self.presentation)

        answer1 = Answer.objects.create(question_id=self.question.id, variant_number=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, variant_number=2, text='No', has_comment=False)
        answer3 = Answer.objects.create(question_id=self.question.id, variant_number=3, text='Nothing', has_comment=False)

        response = self.client.get(reverse('slide_view', kwargs={'slide': self.slide.id}))
        self.assertInHTML(needle='<input type="checkbox" name="group1" value="{}">'.format(answer1.id), haystack=response.rendered_content)
        self.assertInHTML(needle='<input type="checkbox" name="group1" value="{}">'.format(answer2.id), haystack=response.rendered_content)
        self.assertInHTML(needle='<input type="checkbox" name="group1" value="{}">'.format(answer3.id), haystack=response.rendered_content)


