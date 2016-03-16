#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from cms.tests import BaseOrgTestCase


class CmsDashboardViewTests(BaseOrgTestCase):

    def setUp(self):
        super(CmsDashboardViewTests, self).setUp()
        self.url = reverse('cms:main', kwargs={'organisation': self.organisation.slug})
        self.response = self.client.get(self.url)

    def test_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_guest_view(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEquals(response.status_code, 200)
