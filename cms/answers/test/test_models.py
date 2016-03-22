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

    def test_get_previous(self):
        question = Question.objects.create(text='test question2', answers_type='single')
        answer = Answer.objects.create(question=question, position=4, text='test1',
                                       is_right=False, has_comment=False)
        self.assertEqual(self.answer_1.get_previous, False)
        self.assertEqual(self.answer_2.get_previous, self.answer_1)
        self.assertEqual(self.answer_3.get_previous, self.answer_2)
        self.assertEqual(answer.get_previous, False)

    def test_get_next(self):
        question = Question.objects.create(text='test question2', answers_type='single')
        answer = Answer.objects.create(question=question, position=4, text='test1',
                                       is_right=False, has_comment=False)
        self.assertEqual(self.answer_1.get_next, self.answer_2)
        self.assertEqual(self.answer_2.get_next, self.answer_3)
        self.assertEqual(self.answer_3.get_next, False)
        self.assertEqual(answer.get_next, False)

    def test_next_and_previous(self):
        self.assertEqual(self.answer_2.get_next, self.answer_3)
        self.assertEqual(self.answer_3.get_previous, self.answer_2)

    def test_auto_last_position(self):
        answer = Answer.objects.create(question=self.question, text='4',
                                       is_right=False, has_comment=False)
        self.assertEqual(answer.position, 4)

    def test_change_position_after_delete(self):
        self.answer_1.delete()
        position_list = []
        for answer in Answer.objects.all():
            position_list.append(answer.position)
        self.assertEqual(position_list, [1, 2])
