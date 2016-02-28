# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase


class QuestionViewTests(TestCase):

    def test_view(self):
        response = self.client.get(reverse('slide_view', kwargs={'slide': '1'}))
        # response = self.client.get('/slides/1')
        self.assertEqual(response.status_code, 200)

