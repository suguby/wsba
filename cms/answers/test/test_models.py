#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase

from presentations.models import Answer, Question


class AnswerTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(text='test question', answers_type='single')
        self.answer_1 = Answer.objects.create(question=self.question, position=1, text='test1',
                                              is_right=False, has_comment=True)
        self.answer_2 = Answer.objects.create(question=self.question, position=2, text='test2',
                                              is_right=False, has_comment=False)
        self.answer_3 = Answer.objects.create(question=self.question, position=3, text='test3',
                                              is_right=False, has_comment=False)

    def test_has_previous(self):
        question = Question.objects.create(text='test question2', answers_type='single')
        answer = Answer.objects.create(question=question, position=1, text='test1',
                                       is_right=False, has_comment=False)
        self.assertEqual(self.answer_1.has_previous, False)
        self.assertEqual(self.answer_2.has_previous, True)
        self.assertEqual(self.answer_3.has_previous, True)
        self.assertEqual(answer.has_previous, False)

    def test_next(self):
        question = Question.objects.create(text='test question2', answers_type='single')
        answer = Answer.objects.create(question=question, position=1, text='test1',
                                       is_right=False, has_comment=False)
        self.assertEqual(self.answer_1.has_next, True)
        self.assertEqual(self.answer_2.has_next, True)
        self.assertEqual(self.answer_3.has_next, False)
        self.assertEqual(answer.has_next, False)

    def test_next_and_previous(self):
        self.assertEqual(self.answer_2.has_next, True)
        self.assertEqual(self.answer_3.has_previous, True)
