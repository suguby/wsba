#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from presentations.models import Organisation, Question


class QuestionViewTestsCase(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')
        self.organisation = Organisation.objects.create(name='test', slug='test')

    def test_list_view(self):
        url = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        question = Question.objects.create(number=1, text='test', answers_type='single')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms/questions/list.html')
        self.assertInHTML(needle='<span class="label label-info">single</span>', haystack=response.rendered_content)
        self.assertContains(response, question.text, status_code=200)

    def test_detail_view(self):
        question = Question.objects.create(number=2, text='test?', answers_type='single')
        url = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                      'question': question.id})
        url_404 = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                          'question': 2})
        response = self.client.get(url)
        response_404 = self.client.get(url_404)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms/questions/detail.html')
        self.assertEqual(response.context['question'].pk, 1)
        self.assertEqual(response.context['question'].number, 2)
        self.assertEqual(response.context['question'].text, 'test?')
        self.assertInHTML(needle='<div class="panel-body">test?</div>', haystack=response.rendered_content)
        self.assertContains(response, question.text, status_code=200)
        self.assertEqual(response_404.status_code, 404)

    def test_create_view(self):
        Question.objects.create(number=3, text='test update', answers_type='single')
        url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        response_get = self.client.get(url)
        response_post = self.client.post(url, {'number': 1, 'text': 'new_question', 'answers_type': 'multi'})
        self.assertEquals(response_get.status_code, 200)
        self.assertContains(response_get, 'Создать', status_code=200)
        self.assertContains(response_get, 'Добавление вопроса', status_code=200)
        self.assertEquals(response_post.status_code, 302)
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Question.objects.get(number=1).text, 'new_question')
        self.assertTemplateUsed(response_get, 'cms/questions/edit.html')

    def test_update_view(self):
        question = Question.objects.create(number=3, text='test update', answers_type='single')
        url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug, 'question': question.id})
        response_get = self.client.get(url)
        response_post = self.client.post(url, {'number': 1000, 'text': 'edit question', 'answers_type': 'multi'})
        form = response_get.context['form']
        self.assertEquals(response_get.status_code, 200)
        self.assertContains(response_get, 'Обновить', status_code=200)
        self.assertContains(response_get, 'Редактирование вопроса', status_code=200)
        self.assertEquals(form['number'].value(), 3)
        self.assertEquals(form['text'].value(), 'test update')
        self.assertEquals(form['answers_type'].value(), 'single')
        self.assertEquals(response_post.status_code, 302)
        self.assertEqual(Question.objects.get(text='edit question').number, 1000)
        self.assertTemplateUsed(response_get, 'cms/questions/edit.html')

    def test_delete_view(self):
        Question.objects.create(number=1, text='test delete', answers_type='single')
        Question.objects.create(number=2, text='test delete 2', answers_type='single')
        question = Question.objects.create(number=3, text='test delete 3', answers_type='single')
        url = reverse('cms:questions-delete', kwargs={'organisation': self.organisation.slug, 'question': question.id})
        response = self.client.post(url)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Question.objects.filter(number=3).count(), 0)
