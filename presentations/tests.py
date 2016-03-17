# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from presentations.models import CoreSlide, Organisation, Presentation, Question, Answer, UserAnswer


class QuestionViewTests(TestCase):
    def setUp(self):
        organisation = Organisation.objects.create(name='Рога и Копыта')
        self.presentation = Presentation.objects.create(organisation=organisation)

    def test_no_question(self):
        self.slide = CoreSlide.objects.create(presentation=self.presentation)

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
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer1.id),
                          haystack=response.rendered_content)
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer2.id),
                          haystack=response.rendered_content)

    def test_single_comment_answer(self):
        self.question = Question.objects.create(number=1, text='Кто виноват?', answers_type='single')
        self.slide = CoreSlide.objects.create(question=self.question, presentation=self.presentation)

        answer1 = Answer.objects.create(question_id=self.question.id, variant_number=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, variant_number=2, text='No', has_comment=True)

        response = self.client.get(reverse('slide_view', kwargs={'slide': self.slide.id}))
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer1.id),
                          haystack=response.rendered_content)
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer2.id),
                          haystack=response.rendered_content)
        self.assertContains(response, "Комментарий:")

    def test_multi_answer(self):
        self.question = Question.objects.create(number=1, text='Кто виноват?', answers_type='multi')
        self.slide = CoreSlide.objects.create(question=self.question, presentation=self.presentation)

        answer1 = Answer.objects.create(question_id=self.question.id, variant_number=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, variant_number=2, text='No', has_comment=False)
        answer3 = Answer.objects.create(question_id=self.question.id, variant_number=3, text='Nothing',
                                        has_comment=False)

        response = self.client.get(reverse('slide_view', kwargs={'slide': self.slide.id}))
        checkbox_html = '<input type="checkbox" name="group1" value="{}">'
        self.assertInHTML(needle=checkbox_html.format(answer1.id), haystack=response.rendered_content)
        self.assertInHTML(needle=checkbox_html.format(answer2.id), haystack=response.rendered_content)
        self.assertInHTML(needle=checkbox_html.format(answer3.id), haystack=response.rendered_content)

    def test_single_answer_saving(self):
        self.question = Question.objects.create(number=1, text='Кто виноват?', answers_type='single')
        self.slide = CoreSlide.objects.create(question=self.question, presentation=self.presentation)

        answer1 = Answer.objects.create(question_id=self.question.id, variant_number=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, variant_number=2, text='No', has_comment=False)

        url = reverse('slide_view', kwargs={'slide': self.slide.id})
        response = self.client.post(url, {'group1': ['2'],})
        self.assertEqual(response.status_code, 302)
        answers = UserAnswer.objects.filter(user_id=1, answer_id=2)
        self.assertEqual(len(answers), 1)

    def test_multi_answer_saving(self):
        self.question = Question.objects.create(number=1, text='Кто виноват?', answers_type='multi')
        self.slide = CoreSlide.objects.create(question=self.question, presentation=self.presentation)

        answer1 = Answer.objects.create(question_id=self.question.id, variant_number=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, variant_number=2, text='No', has_comment=False)

        url = reverse('slide_view', kwargs={'slide': self.slide.id})
        response = self.client.post(url, {'group1': ['2'],})
        self.assertEqual(response.status_code, 302)
        answers = UserAnswer.objects.filter(user_id=1, answer_id=2)
        self.assertEqual(len(answers), 1)

    def test_single_answer_comment_saving(self):
        self.question = Question.objects.create(number=1, text='Кто виноват?', answers_type='single')
        self.slide = CoreSlide.objects.create(question=self.question, presentation=self.presentation)

        answer1 = Answer.objects.create(question_id=self.question.id, variant_number=1, text='Yes', has_comment=True)
        answer2 = Answer.objects.create(question_id=self.question.id, variant_number=2, text='No', has_comment=False)

        url = reverse('slide_view', kwargs={'slide': self.slide.id})
        response = self.client.post(url, {'group1': ['1'], 'comment': 'some text'})
        self.assertEqual(response.status_code, 302)
        answers = UserAnswer.objects.filter(user_id=1, answer_id=1)
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0].comment, 'some text')

