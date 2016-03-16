#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from cms.questions.test.common import BaseOrgTestCase, BaseQuestionTestCase
from presentations.models import Question


class CmsQuestionListViewTests(BaseOrgTestCase):

    def test_view(self):
        response = self.client.get(reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug}))
        self.assertEqual(response.status_code, 200)
        self.question = Question.objects.create(number=1, text='test')


class CmsQuestionDetailViewTests(BaseQuestionTestCase):

    def test_view(self):
        response = self.client.get(reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                                           'question': self.question.id}))
        self.assertEqual(response.status_code, 200)


class CmsQuestionEditViewTests(BaseQuestionTestCase):

    def test_get_view(self):
        response = self.client.get(reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug,
                                                                         'question': self.question.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_view(self):
        response = self.client.post(reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug,
                                                                          'question': self.question.id}))
        self.assertEqual(response.status_code, 200)


class CmsQuestionAddViewTests(BaseQuestionTestCase):

    def test_get_view(self):
        response = self.client.get(reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug}))
        self.assertEqual(response.status_code, 200)

    def test_post_view(self):
        response = self.client.post(reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug}))
        self.assertEqual(response.status_code, 200)

# class CmsQuestionDeleteViewTests(BaseQuestionTestCase):
#
#     def test_post_view(self):
#         response = self.client.post(reverse('cms:questions-delete', kwargs={'organisation': self.organisation.slug,
#                                                                             'question': self.question.id}))
#         self.assertEqual()

