# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from presentations.models import CoreSlide, Organisation, Presentation, Question, Answer, UserAnswer


class QuestionViewTests(TestCase):

    def setUp(self):
        self.organisation = Organisation.objects.create(name='Рога и Копыта')
        self.presentation = Presentation.objects.create(organisation=self.organisation)
        self.slide = CoreSlide.objects.create(presentation=self.presentation)
        self.url = reverse('slide_view', kwargs={'slide': self.slide.id})

    def test_no_question(self):
        response = self.client.get(self.url)
        self.assertInHTML(needle='<form method="post" action="">', haystack=response.rendered_content, count=0)


class QuestionSingleViewTests(QuestionViewTests):

    def setUp(self):
        super().setUp()
        self.question = Question.objects.create(text='Кто виноват?', answers_type='single')
        self.slide.question = self.question
        self.slide.save()

    def test_has_question(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.text)

    def test_single_answer(self):
        answer1 = Answer.objects.create(question_id=self.question.id, position=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, position=2, text='No', has_comment=False)

        response = self.client.get(self.url)
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer1.id),
                          haystack=response.rendered_content)
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer2.id),
                          haystack=response.rendered_content)

    def test_single_commented_answer(self):
        answer1 = Answer.objects.create(question_id=self.question.id, position=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, position=2, text='No', has_comment=True)

        response = self.client.get(self.url)
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer1.id),
                          haystack=response.rendered_content)
        self.assertInHTML(needle='<input type="radio" name="group1" value="{}">'.format(answer2.id),
                          haystack=response.rendered_content)
        self.assertContains(response, "Комментарий:")  # тоже хрупко - вдруг в шаблоне поменяется слово? я бы html-элемент искал поле для воода комментария с определенным именем

    def test_single_answer_saving(self):
        answer1 = Answer.objects.create(question_id=self.question.id, position=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, position=2, text='No', has_comment=False)

        response = self.client.post(self.url, {'group1': [answer2.id], })
        self.assertEqual(response.status_code, 302)
        answers = UserAnswer.objects.filter(user_id=1, answer_id=answer2.id)
        self.assertEqual(len(answers), 1)

    def test_single_answer_commented_saving(self):
        answer1 = Answer.objects.create(question_id=self.question.id, position=1, text='Yes', has_comment=True)
        answer2 = Answer.objects.create(question_id=self.question.id, position=2, text='No', has_comment=False)

        response = self.client.post(self.url, {'group1': [answer1.id], 'comment': 'some text'})
        self.assertEqual(response.status_code, 302)
        answers = UserAnswer.objects.filter(user_id=1, answer_id=answer1.id)
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0].comment, 'some text')

    def test_view_old_single_answer(self):
        answer1 = Answer.objects.create(question_id=self.question.id, position=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, position=2, text='No', has_comment=False)

        user_answer = UserAnswer.objects.create(user_id=1, answer_id=answer1.id)

        response = self.client.get(self.url)
        self.assertInHTML(needle='<input type="radio" name="group1" value="{0}" checked="1">'.format(answer1.id),
                          haystack=response.rendered_content)

    def test_view_old_single_commented_answer(self):
        answer1 = Answer.objects.create(question_id=self.question.id, position=1, text='Yes', has_comment=True)
        answer2 = Answer.objects.create(question_id=self.question.id, position=2, text='No', has_comment=False)

        user_answer = UserAnswer.objects.create(user_id=1, answer_id=answer1.id, comment="Это комментарий!")

        response = self.client.get(self.url)
        self.assertInHTML(needle='<input type="radio" name="group1" value="{0}" checked="1">'.format(answer1.id),
                          haystack=response.rendered_content)
        self.assertContains(response, "Это комментарий!")


class QuestionMultiViewTests(QuestionViewTests):

    def setUp(self):
        super().setUp()
        self.question = Question.objects.create(text='Что делать?', answers_type='multi')
        self.slide.question = self.question
        self.slide.save()

    def test_multi_answer(self):
        answer1 = Answer.objects.create(question_id=self.question.id, position=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, position=2, text='No', has_comment=False)
        answer3 = Answer.objects.create(question_id=self.question.id, position=3, text='Nothing',
                                        has_comment=False)

        response = self.client.get(self.url)
        checkbox_html = '<input type="checkbox" name="group1" value="{}">'
        self.assertInHTML(needle=checkbox_html.format(answer1.id), haystack=response.rendered_content)
        self.assertInHTML(needle=checkbox_html.format(answer2.id), haystack=response.rendered_content)
        self.assertInHTML(needle=checkbox_html.format(answer3.id), haystack=response.rendered_content)

    def test_multi_answer_saving(self):
        answer1 = Answer.objects.create(question_id=self.question.id, position=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, position=2, text='No', has_comment=False)

        response = self.client.post(self.url, {'group1': [answer2.id, answer1.id,]})
        self.assertEqual(response.status_code, 302)
        answers = UserAnswer.objects.filter(user_id=1)
        self.assertEqual(len(answers), 2)

    def test_view_old_multi_answer(self):
        answer1 = Answer.objects.create(question_id=self.question.id, position=1, text='Yes', has_comment=False)
        answer2 = Answer.objects.create(question_id=self.question.id, position=2, text='No', has_comment=False)

        user_answer = UserAnswer.objects.create(user_id=1, answer_id=answer1.id)

        response = self.client.get(self.url)
        self.assertInHTML(needle='<input type="checkbox" name="group1" value="{0}" checked="1">'.format(answer1.id),
                          haystack=response.rendered_content)

