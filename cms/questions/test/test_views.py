#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from presentations.models import Organisation, Question
from cms.test import BaseTests


class QuestionListViewTests(BaseTests):

    def setUp(self):
        super(QuestionListViewTests, self).setUp()
        self.question = Question.objects.create(text='test3', answers_type='single')
        self.question_2 = Question.objects.create(text='test', answers_type='single')
        self.question_3 = Question.objects.create(text='test2', answers_type='single')
        self.url = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        self.response = self.client.get(self.url)

    def test_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.response.status_code, 200)

    def test_test_template(self):
        questions = Question.objects.all()
        success_url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        self.assertTemplateUsed(self.response, 'cms/questions/list.html')
        self.assertEqual(len(questions), len(self.response.context['object_list']))
        self.assertContains(self.response, self.question.text, status_code=200)
        self.assertNotIn('back_button', self.response.context)
        self.assertIn('add_button', self.response.context)
        self.assertNotIn('edit_button', self.response.context)
        self.assertNotIn('del_button', self.response.context)
        self.assertEqual(success_url, self.response.context['add_button'])
        self.assertContains(self.response, 'id="add_button"', status_code=200)


class QuestionDetailViewTests(BaseTests):
    
    def setUp(self):
        super(QuestionDetailViewTests, self).setUp()
        self.question = Question.objects.create(text='test?', answers_type='single')
        self.url = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                           'question': self.question.id})
        self.response = self.client.get(self.url)

    def test_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.response.status_code, 200)

    def test_not_get_object(self):
        url_404 = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                          'question': 100})
        response_404 = self.client.get(url_404)
        self.assertEqual(response_404.status_code, 404)

    def test_template(self):
        url_back = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        url_add = reverse('cms:answers-add', kwargs={'organisation': self.organisation.slug,
                                                     'question': self.question.id})
        url_edit = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug,
                                                         'question': self.question.id})
        url_delete = reverse('cms:questions-delete', kwargs={'organisation': self.organisation.slug,
                                                             'question': self.question.id})
        self.assertEqual(url_back, self.response.context['back_button'])
        self.assertEqual(url_add, self.response.context['add_button'])
        self.assertEqual(url_edit, self.response.context['edit_button'])
        self.assertEqual(url_delete, self.response.context['del_button'])
        self.assertEqual(self.question, self.response.context['object'])
        self.assertTemplateUsed(self.response, 'cms/questions/detail.html')
        self.assertContains(self.response, self.question.text, status_code=200)
        self.assertIn('back_button', self.response.context)
        self.assertIn('add_button', self.response.context)
        self.assertIn('edit_button', self.response.context)
        self.assertIn('del_button', self.response.context)
        self.assertEqual(url_back, self.response.context['back_button'])
        self.assertEqual(url_add, self.response.context['add_button'])
        self.assertEqual(url_edit, self.response.context['edit_button'])
        self.assertEqual(url_delete, self.response.context['del_button'])
        self.assertContains(self.response, 'id="back_button"', status_code=200)
        self.assertContains(self.response, 'id="add_button"', status_code=200)
        self.assertContains(self.response, 'id="edit_button"', status_code=200)
        self.assertContains(self.response, 'id="del_button"', status_code=200)


class QuestionCreateViewTests(BaseTests):

    def setUp(self):
        super(QuestionCreateViewTests, self).setUp()
        self.question = Question.objects.create(text='test update', answers_type='single')
        self.url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        self.response = self.client.get(self.url)

    def test_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.response.status_code, 200)

    def test_template(self):
        url_back = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        self.assertIn('form', self.response.context)
        self.assertTemplateUsed(self.response, 'cms/questions/edit.html')
        self.assertContains(self.response, 'Создать', status_code=200)
        self.assertContains(self.response, 'Добавление вопроса', status_code=200)
        self.assertIn('back_button', self.response.context)
        self.assertNotIn('add_button', self.response.context)
        self.assertNotIn('edit_button', self.response.context)
        self.assertNotIn('del_button', self.response.context)
        self.assertEqual(url_back, self.response.context['back_button'])
        self.assertContains(self.response, 'id="back_button"', status_code=200)

    def test_post_status_valid(self):
        Question.objects.create(text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        response = self.client.post(url, {'text': 'new_question', 'answers_type': 'multi'})
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        Question.objects.create(text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        response = self.client.post(url, {'text': 'new_question'})
        self.assertNotEquals(response.status_code, 302)

    def test_post_add_object(self):
        Question.objects.create(text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        self.client.post(url, {'text': 'new_question', 'answers_type': 'multi'})
        self.assertEqual(Question.objects.count(), 3)
        self.assertEqual(Question.objects.filter(text='new_question').count(), 1)


class QuestionEditViewTests(BaseTests):

    def setUp(self):
        super(QuestionEditViewTests, self).setUp()
        self.question = Question.objects.create(text='test update', answers_type='single')
        self.url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug,
                                                         'question': self.question.id})
        self.response = self.client.get(self.url)

    def test_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.response.status_code, 200)

    def test_template(self):
        self.assertEqual(self.question.id, self.response.context['object'].id)
        self.assertTemplateUsed(self.response, 'cms/questions/edit.html')
        self.assertContains(self.response, 'Обновить', status_code=200)
        self.assertContains(self.response, 'Редактирование вопроса', status_code=200)
        self.assertContains(self.response, self.question.text, status_code=200)
        self.assertContains(self.response, self.question.answers_type, status_code=200)
        self.assertIn('back_button', self.response.context)
        self.assertNotIn('add_button', self.response.context)
        self.assertNotIn('edit_button', self.response.context)
        self.assertNotIn('del_button', self.response.context)
        back_url = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                           'question': self.question.id})
        self.assertEqual(back_url, self.response.context['back_button'])
        self.assertContains(self.response, 'id="back_button"', status_code=200)

    def test_post_status_valid(self):
        question = Question.objects.create(text='test update', answers_type='single')
        url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug,
                                                    'question': question.id})
        response = self.client.post(url, {'text': 'edit question', 'answers_type': 'multi'})
        self.assertEquals(response.status_code, 302)

    def test_post_status_invalid(self):
        question = Question.objects.create(text='test update', answers_type='single')
        url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug,
                                                    'question': question.id})
        response = self.client.post(url, {'text': '1'})
        self.assertNotEquals(response.status_code, 302)

    def test_post_edit_object(self):
        question = Question.objects.create(text='testing', answers_type='single')
        url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug,
                                                    'question': question.id})
        self.client.post(url, {'text': 'edit question', 'answers_type': 'multi'})
        self.assertEqual(Question.objects.filter(text='testing').count(), 0)


class QuestionDeleteViewTests(BaseTests):

    def setUp(self):
        super(QuestionDeleteViewTests, self).setUp()
        self.question = Question.objects.create(text='test delete', answers_type='single')
        self.question_2 =Question.objects.create(text='test delete 2', answers_type='single')
        self.question_3 = Question.objects.create(text='test delete 3', answers_type='single')
        self.url = reverse('cms:questions-delete', kwargs={'organisation': self.organisation.slug,
                                                           'question': self.question.id})
        self.response = self.client.post(self.url)

    def test_post_status_valid(self):
        self.assertEquals(self.response.status_code, 302)

    def test_post_status_invalid(self):
        url = reverse('cms:questions-delete', kwargs={'organisation': self.organisation.slug, 'question': 10})
        response = self.client.post(url)
        self.assertNotEquals(response.status_code, 302)

    def test_delete_object(self):
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Question.objects.filter(text='test delete').count(), 0)
