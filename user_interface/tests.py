# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import ProjectUser
from presentations.models import Organisation, Presentation
from presentations.models import CoreSlide


# Create your tests here.


class PresentationsView(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name='testorg', slug='testorg')
        self.user = ProjectUser.objects.create(name='tester1', organisation=self.org)

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
        self.slide = CoreSlide.objects.create(presentation=self.presentation_1, position=0)
        self.url = reverse(viewname='organisation_detail', kwargs=dict(organisation=self.org.slug, ))
        self.url_detail = reverse(viewname='presentation_begin',
                                  kwargs=dict(organisation=self.org.slug, presentation_id=self.presentation_1.id))

    def test_presentations_view(self):
        response = self.client.get(self.url)
        self.assertContains(response, status_code=200, text='tester')
        self.assertContains(response, status_code=200, text=self.org.slug)
        self.assertContains(response, status_code=200, text=self.presentation_1.name)
        self.assertContains(response, status_code=200, text=self.presentation_2.name)

    def test_presentations_butons_view(self):
        response = self.client.get(self.url)
        self.assertContains(response, status_code=200, text='посмотреть', count=2)
        self.assertInHTML(
                needle='<a href="/{}/presentation/{}/">посмотреть</a>'.format(self.org.slug, self.presentation_1.id),
                haystack=response.rendered_content)
        self.assertInHTML(
                needle='<a href="/{}/presentation/{}/">посмотреть</a>'.format(self.org.slug, self.presentation_2.id),
                haystack=response.rendered_content)


class PresentationsDetails(PresentationsView):
    def setUp(self):
        super().setUp()

    def test_detail(self):
        response = self.client.get(self.url_detail)
        self.assertContains(response, status_code=200, text=self.org.slug)
        self.assertContains(response, status_code=200, text=self.presentation_1.description)
        self.assertContains(response, status_code=200, text='Начать')
        self.assertInHTML(
                needle='<a class="btn btn-default left" role="button" href="/{}/presentation/{}/slides/{}">Начать</a>'.format(
                    self.org.slug,
                    self.presentation_1.id,
                    CoreSlide.objects.filter(presentation_id=self.presentation_1.id).order_by('position')[0].id),
                haystack=response.rendered_content)
