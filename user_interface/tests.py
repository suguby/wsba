# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import ProjectUser
from presentations.models import Organisation, Presentation
# Create your tests here.


class ProjectUserTestCase(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name='testorg', slug='testorg')
        self.user = ProjectUser.objects.create(name="username", organisation=self.org)


    def test_presentations(self):
            presentation_1 = Presentation.objects.create(organisation=self.org, name='test_presentation1')
            presentation_2 = Presentation.objects.create(organisation=self.org, name='test_presentation2')
            response = self.client.get(reverse(viewname='organisation_detail', kwargs=dict(organisation=self.org.slug)))
            self.assertContains(response, status_code=200, text=presentation_1.name)
            self.assertContains(response, status_code=200, text=presentation_2.name)