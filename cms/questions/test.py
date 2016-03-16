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
        self.url = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        self.question = Question.objects.create(number=1, text='test', answers_type='single')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertInHTML(needle='<span class="label label-info">single</span>', haystack=response.rendered_content)
        self.assertTemplateUsed(response, 'cms/questions/list.html')

    def test_detail_view(self):
        pass

    def test_create_view(self):
        pass

    def test_update_view(self):
        pass

    def test_delete_view(self):
        pass

