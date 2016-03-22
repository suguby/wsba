#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase

from presentations.models import Organisation


class BaseTests(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        self.client.login(username='admin', password='admin')
        self.organisation = Organisation.objects.create(name='test', slug='test')