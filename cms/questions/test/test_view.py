#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from cms.tests import BaseQuestionTestCase, BaseQuestionListView, BaseQuestionGuestListView

# как лучше? CmsQuestionListViewTests или как CmsQuestionUserListViewTests и CmsQuestionGuestListViewTests или тут треш везде ?
# дальше пока трогать не стал


class CmsQuestionListViewTests(BaseQuestionListView):

    def test_user_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_guest_view(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEquals(response.status_code, 200)


class CmsQuestionUserListViewTests(BaseQuestionListView):

    def test_view(self):
        self.assertEqual(self.response.status_code, 200)


class CmsQuestionGuestListViewTests(BaseQuestionGuestListView):

    def test_view(self):
        self.assertNotEquals(self.response.status_code, 200)


class CmsQuestionDetailViewTests(BaseQuestionTestCase):

    def setUp(self):
        super(CmsQuestionDetailViewTests, self).setUp()
        self.url = reverse('cms:questions-detail', kwargs={'organisation': self.organisation.slug,
                                                           'question': self.question.id})
        self.response = self.client.get(self.url)

    def test_user_view(self):
        self.assertEqual(self.response.status_code, 200)

    def test_guest_view(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEquals(response.status_code, 200)


class CmsQuestionEditViewTests(BaseQuestionTestCase):

    def setUp(self):
        super(CmsQuestionEditViewTests, self).setUp()
        self.url = reverse('cms:questions-edit', kwargs={'organisation': self.organisation.slug,
                                                         'question': self.question.id})
        self.response_get = self.client.get(self.url)
        self.response_post = self.client.post(self.url)

    def test_user_get_view(self):
        self.assertEqual(self.response_get.status_code, 200)

    def test_guest_get_view(self):
        self.client.logout()
        response_get = self.client.get(self.url)
        self.assertNotEquals(response_get.status_code, 200)

    def test_user_post_view(self):
        self.assertEqual(self.response_get.status_code, 200)

    def test_guest_post_view(self):
        self.client.logout()
        response_post = self.client.post(self.url)
        self.assertNotEqual(response_post.status_code, 200)


class CmsQuestionAddViewTests(BaseQuestionTestCase):

    def setUp(self):
        super(CmsQuestionAddViewTests, self).setUp()
        self.url = reverse('cms:questions-add', kwargs={'organisation': self.organisation.slug})
        self.response_get = self.client.get(self.url)
        self.response_post = self.client.post(self.url)

    def test_user_get_view(self):
        self.assertEqual(self.response_get.status_code, 200)

    def test_guest_get_view(self):
        self.client.logout()
        response_get = self.client.get(self.url)
        self.assertNotEqual(response_get.status_code, 200)

    def test_user_post_view(self):
        self.assertEqual(self.response_post.status_code, 200)

    def test_guest_post_view(self):
        self.client.logout()
        response_post = self.client.post(self.url)
        self.assertNotEqual(response_post.status_code, 200)


class CmsQuestionDeleteViewTests(BaseQuestionTestCase):

    def setUp(self):
        super(CmsQuestionDeleteViewTests, self).setUp()
        self.url = reverse('cms:questions-delete', kwargs={'organisation': self.organisation.slug,
                                                           'question': self.question.id})
        self.response_post = self.client.post(self.url)

    def test_post_view(self):
        self.assertEqual(self.response_post.url,
                         reverse('cms:questions-list', kwargs={'organisation': self.organisation.slug}))


