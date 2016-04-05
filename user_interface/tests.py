# -*- coding: utf-8 -*-

from django.test import TestCase
from .models import ProjectUser
from presentations.models import Organisation
# Create your tests here.


class ProjectUserTestCase(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name='testorg')
        self.user = ProjectUser.objects.create(name="username", organisation=self.org)


def test_presentations(self):
        self.org.id
        self.user.id