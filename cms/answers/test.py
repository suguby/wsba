#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from presentations.models import Organisation, Question, Answer


class AnswerViewTestsCase(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')
        self.organisation = Organisation.objects.create(name='test', slug='test')

    def test_edit_view(self):
        question = Question.objects.create(number=2, text='test?', answers_type='single')
        Answer.objects.create(question=question, variant_number=1, text='test',
                              is_right=True, has_comment=True)
        answer = Answer.objects.create(question=question, variant_number=10, text='test',
                                       is_right=False, has_comment=False)
        url = reverse('cms:answers-edit', kwargs={'organisation': self.organisation.slug,
                                                  'question': question.id, 'answer': answer.id})
        response_get = self.client.get(url)
        form = response_get.context['form']
        response_post = self.client.post(url, {'variant_number': 1000, 'text': 'test edit',
                                               'is_right': True, 'has_comment': True, 'question': question.id})

        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'cms/answers/edit.html')
        self.assertContains(response_get, 'Обновить', status_code=200)
        self.assertContains(response_get, 'Редактирование ответа', status_code=200)
        self.assertContains(response_get, question.number, status_code=200)
        self.assertContains(response_get, question.text, status_code=200)
        self.assertContains(response_get, answer.variant_number, status_code=200)
        self.assertContains(response_get, answer.text, status_code=200)
        self.assertContains(response_get, 'Правильный', status_code=200)
        self.assertContains(response_get, 'С комментарием', status_code=200)
        self.assertEquals(form['variant_number'].value(), 10)
        self.assertEquals(form['text'].value(), answer.text)
        self.assertEquals(form['is_right'].value(), answer.is_right)
        self.assertEquals(form['has_comment'].value(), answer.has_comment)
        self.assertEquals(form['question'].value(), answer.question.pk)

        self.assertEquals(response_post.status_code, 302)
        self.assertEqual(Answer.objects.filter(variant_number=10).count(), 0)
        self.assertEqual(Answer.objects.get(text='test edit').pk, 2)

        self.assertIn('back_button', response_get.context)
        self.assertEqual(reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                                 'question': question.id}),
                         response_get.context['back_button'])
        self.assertContains(response_get, 'id="back_button"', status_code=200)
        self.assertNotIn('add_button', response_get.context)
        self.assertNotIn('edit_button', response_get.context)
        self.assertIn('del_button', response_get.context)
        self.assertEqual(reverse('cms:answers-delete', kwargs={'organisation': self.organisation.slug,
                                                               'question': question.id, 'answer': answer.id}),
                         response_get.context['del_button'])
        self.assertContains(response_get, 'id="del_button"', status_code=200)

    def test_create_view(self):
        question = Question.objects.create(number=2, text='test?', answers_type='single')
        Answer.objects.create(question=question, variant_number=1, text='test',
                              is_right=False, has_comment=True)
        Answer.objects.create(question=question, variant_number=2, text='test2',
                              is_right=False, has_comment=False)
        url = reverse('cms:answers-add', kwargs={'organisation': self.organisation.slug,
                                                 'question': question.id})
        response_get = self.client.get(url)
        response_post = self.client.post(url, {'variant_number': 3, 'text': 'new',
                                               'is_right': True, 'has_comment': True, 'question': question.id})

        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'cms/answers/edit.html')

        self.assertContains(response_get, 'Создать', status_code=200)
        self.assertContains(response_get, 'Добавление ответа', status_code=200)
        self.assertContains(response_get, question.number, status_code=200)
        self.assertContains(response_get, question.text, status_code=200)
        self.assertContains(response_get, 'С комментарием', status_code=200)
        self.assertEqual(response_get.context['question'].pk, question.id)

        self.assertEquals(response_post.status_code, 302)
        self.assertEqual(Answer.objects.filter(variant_number=3).count(), 1)
        self.assertEqual(Answer.objects.get(text='new').is_right, True)

        self.assertIn('back_button', response_get.context)
        self.assertEqual(reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                                 'question': question.id}),
                         response_get.context['back_button'])
        self.assertContains(response_get, 'id="back_button"', status_code=200)
        self.assertNotIn('add_button', response_get.context)
        self.assertNotIn('edit_button', response_get.context)
        self.assertNotIn('del_button', response_get.context)

    def test_delete_view(self):
        question = Question.objects.create(number=2, text='test?', answers_type='single')
        Answer.objects.create(question=question, variant_number=1, text='test',
                              is_right=False, has_comment=True)
        answer = Answer.objects.create(question=question, variant_number=2, text='test2',
                                       is_right=False, has_comment=False)
        url = reverse('cms:answers-edit', kwargs={'organisation': self.organisation.slug,
                                                  'question': question.id, 'answer': answer.id})
        response = self.client.post(url, {'variant_number': 3, 'text': 'new',
                                          'is_right': True, 'has_comment': True, 'question': question.id})

        self.assertEquals(response.status_code, 302)
        self.assertEqual(Answer.objects.filter(question=question).count(), 1)
        self.assertEqual(Answer.objects.filter(variant_number=2, question=question).count(), 0)
