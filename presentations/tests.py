# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from presentations.models import CoreSlide, Organisation, Presentation, Question


class QuestionViewTests(TestCase):

    def test_view(self):
        organisation = Organisation.objects.create(name='ldsfl')
        presentation = Presentation.objects.create(organisation=organisation)
        question = Question.objects.create(text='dsfds')
        slide = CoreSlide.objects.create(question=question, presentation=presentation)

        response = self.client.get(reverse('slide_view', kwargs={'slide': slide.id}))
        self.assertEqual(response.status_code, 200)
        #  TODO проверить что отобразился именно нужный слайд - по содержимому ответа

