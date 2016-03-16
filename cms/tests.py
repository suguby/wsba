# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from presentations.models import Organisation, Question


class BaseUserTestCase(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')


class BaseOrgTestCase(BaseUserTestCase):

    def setUp(self):
        super(BaseOrgTestCase, self).setUp()
        self.organisation = Organisation.objects.create(name='test', slug='test')


class BaseQuestionTestCase(BaseOrgTestCase):

    def setUp(self):
        super(BaseQuestionTestCase, self).setUp()
        self.question = Question.objects.create(number=1, text='test')


class BaseQuestionGuestTestCase(BaseOrgTestCase):

    def setUp(self):
        super(BaseQuestionGuestTestCase, self).setUp()
        self.question = Question.objects.create(number=1, text='test')
        self.client.logout()


class BaseQuestionListView(BaseQuestionTestCase):

    def setUp(self):
        super(BaseQuestionListView, self).setUp()
        self.url = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        self.response = self.client.get(self.url)


class BaseQuestionGuestListView(BaseQuestionTestCase):

    def setUp(self):
        super(BaseQuestionGuestListView, self).setUp()
        self.client.logout()
        self.url = reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug})
        self.response = self.client.get(self.url)
