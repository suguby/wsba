#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase

from presentations.models import Organisation, Question


class BaseLoginTestCase(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')


class BaseOrgTestCase(BaseLoginTestCase):

    def setUp(self):
        super(BaseOrgTestCase, self).setUp()
        self.organisation = Organisation.objects.create(name='test', slug='test')


class BaseQuestionTestCase(BaseOrgTestCase):

    def setUp(self):
        super(BaseQuestionTestCase, self).setUp()
        self.question = Question.objects.create(number=1, text='test')