#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from cms.test import BaseTests


class DashboardViewTests(BaseTests):

    def setUp(self):
        super(DashboardViewTests, self).setUp()
        self.url = reverse('cms:main',
                           kwargs={'organisation': self.organisation.slug})
        self.response = self.client.get(self.url)

    def test_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'cms/dashboard/index.html')
        self.assertEqual(self.organisation,
                         self.response.context['organisation'])
