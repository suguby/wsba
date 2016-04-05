#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase

from presentations.models import Presentation, Organisation


class AnswerTest(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(name='test',
                                                        slug='test')
        self.presentation = Presentation.objects.\
            create(organisation=self.organisation, name='test presentation',
                   slug='test-presentation')

    def test_save(self):
        presentation = Presentation.objects.\
            create(organisation=self.organisation, name='second presentation',
                   slug='second-presentation')
        self.assertEqual(presentation.position, 2)
