#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from cms.questions.test.test_view import BaseTests
from presentations.models import Question, Answer


class AnswerEditViewTests(BaseTests):

    def setUp(self):
        super(AnswerEditViewTests, self).setUp()
        self.question = Question.objects.create(text='test?', answers_type='single')
        self.answer = Answer.objects.create(question=self.question, text='test',
                                            is_right=True, has_comment=True)
        self.answer_2 = Answer.objects.create(question=self.question, text='test',
                                              is_right=False, has_comment=False)
        self.url = reverse('cms:answers-edit', kwargs={'organisation': self.organisation.slug,
                                                       'question': self.question.id, 'answer': self.answer.id})
        self.response = self.client.get(self.url)

    def test_template(self):
        hidden_input = '<input id="id_question" name="question" type="hidden" value="{}" />'.format(self.question.id)
        back_url = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                           'question': self.question.id})
        del_url = reverse('cms:answers-delete', kwargs={'organisation': self.organisation.slug,
                                                        'question': self.question.id, 'answer': self.answer.id})
        self.assertTemplateUsed(self.response, 'cms/answers/edit.html')
        self.assertIn('form', self.response.context)
        self.assertInHTML(needle=hidden_input, haystack=self.response.rendered_content)
        self.assertContains(self.response, 'Обновить', status_code=200)
        self.assertContains(self.response, 'Редактирование ответа', status_code=200)
        self.assertContains(self.response, self. question.text, status_code=200)
        self.assertContains(self.response, self.answer.text, status_code=200)
        self.assertContains(self.response, 'Правильный', status_code=200)
        self.assertContains(self.response, 'С комментарием', status_code=200)
        self.assertIn('back_button', self.response.context)
        self.assertNotIn('add_button', self.response.context)
        self.assertNotIn('edit_button', self.response.context)
        self.assertIn('del_button', self.response.context)
        self.assertEqual(back_url, self.response.context['back_button'])
        self.assertEqual(del_url, self.response.context['del_button'])
        self.assertContains(self.response, 'id="back_button"', status_code=200)
        self.assertContains(self.response, 'id="del_button"', status_code=200)

    def test_post_status_valid(self):
        url = reverse('cms:answers-edit', kwargs={'organisation': self.organisation.slug,
                                                  'question': self.question.id, 'answer': self.answer.id})
        response = self.client.post(url, {'text': 'test edit',
                                          'is_right': True, 'has_comment': True, 'question': self.question.id})
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        url = reverse('cms:answers-edit', kwargs={'organisation': self.organisation.slug,
                                                  'question': self.question.id, 'answer': self.answer.id})
        response = self.client.post(url, {'text': 'test edit',
                                          'is_right': True, 'has_comment': True})
        self.assertNotEquals(response.status_code, 302)

    def test_post_edit_object(self):
        self.client.post(self.url, {'text': 'test edit',
                                    'is_right': True, 'has_comment': True, 'question': self.question.id})
        self.assertEqual(Answer.objects.filter(text='test edit').count(), 1)


class AnswerAddViewTests(BaseTests):

    def setUp(self):
        super(AnswerAddViewTests, self).setUp()
        self.question = Question.objects.create(text='test?', answers_type='single')
        self.answer = Answer.objects.create(question=self.question, text='test',
                                            is_right=False, has_comment=True)
        self.answer_2 = Answer.objects.create(question=self.question, text='test2',
                                              is_right=False, has_comment=False)
        self.url = reverse('cms:answers-add', kwargs={'organisation': self.organisation.slug,
                                                      'question': self.question.id})
        self.response = self.client.get(self.url)

    def test_template(self):
        hidden_input = '<input id="id_question" name="question" type="hidden" value="{}" />'.format(self.question.id)
        url_back = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                           'question': self.question.id})

        self.assertTemplateUsed(self.response, 'cms/answers/edit.html')
        self.assertIn('form', self.response.context)
        self.assertInHTML(needle=hidden_input, haystack=self.response.rendered_content)
        self.assertEqual(self.response.context['question'].pk, self.question.id)
        self.assertContains(self.response, 'Создать', status_code=200)
        self.assertContains(self.response, 'Добавление ответа', status_code=200)
        self.assertContains(self.response, self.question.text, status_code=200)
        self.assertContains(self.response, 'С комментарием', status_code=200)
        self.assertIn('back_button', self.response.context)
        self.assertNotIn('add_button', self.response.context)
        self.assertNotIn('edit_button', self.response.context)
        self.assertNotIn('del_button', self.response.context)
        self.assertEqual(url_back, self.response.context['back_button'])
        self.assertContains(self.response, 'id="back_button"', status_code=200)

    def test_post_status_valid(self):
        response = self.client.post(self.url, {'text': 'new',
                                               'is_right': True, 'has_comment': True, 'question': self.question.id})
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        response = self.client.post(self.url, {'text': 'new',
                                               'is_right': True, 'has_comment': True})
        self.assertNotEquals(response.status_code, 302)

    def test_post_edit_object(self):
        self.client.post(self.url, {'text': 'new',
                                    'is_right': True, 'has_comment': True, 'question': self.question.id})
        self.assertEqual(Answer.objects.get(text='new').is_right, True)


class AnswerDeleteViewTests(BaseTests):

    def setUp(self):
        super(AnswerDeleteViewTests, self).setUp()
        self.question = Question.objects.create(text='test?', answers_type='single')
        self.answer = Answer.objects.create(question=self.question, text='test',
                                            is_right=False, has_comment=True)
        self.answer_2 = Answer.objects.create(question=self.question, text='test2',
                                              is_right=False, has_comment=False)
        self.url = reverse('cms:answers-delete', kwargs={'organisation': self.organisation.slug,
                                                         'question': self.question.id, 'answer': self.answer.id})
        self.response = self.client.post(self.url, {'position': 3, 'text': 'new',
                                                    'is_right': True, 'has_comment': True,
                                                    'question': self.question.id})

    def test_post_status_valid(self):
        self.assertEquals(self.response.status_code, 302)

    def test_post_status_invalid(self):
        url = reverse('cms:answers-delete', kwargs={'organisation': self.organisation.slug,
                                                    'question': self.question.id, 'answer': 100})
        response = self.client.post(url)
        self.assertNotEquals(response.status_code, 302)

    def test_delete_object(self):
        self.assertEqual(Answer.objects.filter(question=self.question).count(), 1)
        self.assertEqual(Answer.objects.filter(position=2, question=self.question).count(), 0)


class PositionAnswerTest(BaseTests):

        def setUp(self):
            super(PositionAnswerTest, self).setUp()
            self.question = Question.objects.create(text='test?', answers_type='single')
            self.answer_1 = Answer.objects.create(question=self.question, text='1',
                                                  is_right=True, has_comment=True)
            self.answer_2 = Answer.objects.create(question=self.question, text='2',
                                                  is_right=True, has_comment=True)
            self.answer_3 = Answer.objects.create(question=self.question, text='3',
                                                  is_right=True, has_comment=True)

        def test_up_position(self):
            url = reverse('cms:answers-up', kwargs={'organisation': self.organisation.slug,
                                                    'question': self.question.id, 'answer': self.answer_2.id})
            self.client.post(url)
            answer_text_list =[]
            for answer in Answer.objects.all():
                answer_text_list.append(answer.text)
            self.assertEqual(answer_text_list, ['2', '1', '3'])

        def test_down_position(self):
            url = reverse('cms:answers-down', kwargs={'organisation': self.organisation.slug,
                                                      'question': self.question.id, 'answer': self.answer_2.id})
            self.client.post(url)
            answer_text_list = []
            for answer in Answer.objects.all():
                answer_text_list.append(answer.text)
            self.assertEqual(answer_text_list, ['1', '3', '2'])
