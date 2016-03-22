#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from presentations.models import Organisation


class BaseTests(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')
        self.organisation = Organisation.objects.create(name='test', slug='test')


class DashboardViewTests(BaseTests):

    def setUp(self):
        super(DashboardViewTests, self).setUp()
        self.url = reverse('cms:main', kwargs={'organisation': self.organisation.slug})
        self.response = self.client.get(self.url)

    def test_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'cms/dashboard/index.html')
        self.assertEqual(self.organisation, self.response.context['organisation'])