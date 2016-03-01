# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from presentations.models import CoreSlide, Organisation, Presentation, Question


class QuestionViewTests(TestCase):

    def test_view(self):
        Organisation.objects.create(name='ldsfl')
        Presentation.objects.create(organisation_id=1)
        Question.objects.create(number=1, text='dsfds')
        CoreSlide.objects.create(question_id=1, presentation_id=1)

        response = self.client.get(reverse('slide_view', kwargs={'slide': 1}))
        # response = self.client.get('/slides/1')
        self.assertEqual(response.status_code, 200)

