# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import ProjectUser
from presentations.models import Organisation, Presentation
# Create your tests here.


class PresentationsListView(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name='testorg', slug='testorg')
        self.user = ProjectUser.objects.create(name='tester1', organisation=self.org)
        self.url = reverse(viewname='organisation_detail', kwargs=dict(organisation=self.org.slug,))
        self.presentation_1 = Presentation.objects.create(
                    organisation=self.org,
                    name='test_presentation1',
                    description='описание 1',
            )
        self.presentation_2 = Presentation.objects.create(
                    organisation=self.org,
                    name='test_presentation2',
                    description='описание 2',
            )

    def test_presentations(self):

        response = self.client.get(self.url)
        self.assertContains(response, status_code=200, text='tester')
        self.assertContains(response, status_code=200, text=self.org.slug)
        self.assertContains(response, status_code=200, text=self.presentation_1.name)
        self.assertContains(response, status_code=200, text=self.presentation_2.name)



class PresentationsButtons(PresentationsListView):

    def test_presentations_detail(self):

        response = self.client.get(self.url)
        self.assertContains(response, status_code=200, text='посмотреть', count=2)
        self.assertInHTML(needle='<a href="/{}/presentation/{}/">посмотреть</a>'.format(self.org.slug, self.presentation_1.id),
                          haystack=response.rendered_content)
        self.assertInHTML(needle='<a href="/{}/presentation/{}/">посмотреть</a>'.format(self.org.slug, self.presentation_2.id),
                          haystack=response.rendered_content)
