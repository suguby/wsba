# -*- coding: utf-8 -*-

from django.test import TestCase
from .models import ProjectUser
from presentations.models import Organisation
# Create your tests here.


class ProjectUserTestCase(TestCase):
    def setUp(self):
        org = self.Organisation.objects.create(name='testorg')
        self.ProjectUser.objects.create(name="username", organisation=org)