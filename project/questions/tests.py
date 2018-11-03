# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from core.models import User
from .models import Question
from categories.models import Category

import questions
import json, factory, mock
from mock import patch
from django.shortcuts import render




class TestQuestionFixtures(TestCase):
    fixtures = ['questions/fixtures/testdata_users.json', 'questions/fixtures/testdata_questions.json', ]

    def setUp(self):
        self.user = User.objects.create(username='test_user', email='test_email')
        self.user.set_password('test_password')
        self.user.save()
        self.client = Client()
        self.question = Question.objects.create(name='test_question', author=self.user)

    def test_with_fixtures(self):
        data = json.load(open('questions/fixtures/testdata_questions.json'))

        for i in range(4):
            self.assertEqual((self.client.get('/questions/{}/detail/'.format(data[i]["pk"]))).status_code, 200)


class TestQuestionMock(TestCase):

    @patch('questions.views.question_content')
    def test_with_mock(self, question_content_mock):
        question_content_mock.return_value = 200
        value = questions.views.question_content()
        self.assertEqual(value, 200)

        self.assertEqual(question_content_mock.call_count, 1)




class TestQuestion(TestCase):

    def setUp(self):

        self.user = User.objects.create(username='test_user', email='test_email')
        self.user.set_password('test_password')
        self.user.save()

        self.client = Client()

        self.question = Question.objects.create(name='test_question', author=self.user)
        #self.category = Category.objects.create(name='test_category')

    def test_question_detail_login(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get('/questions/{}/detail/'.format(self.question.pk))
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/questions/{}/detail/'.format(5))
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/questions/create/')
        self.assertEqual(response.status_code, 200)

    def test_question_detail_logout(self):
        self.client.logout()
        response = self.client.get('/questions/{}/detail/'.format(self.question.pk))
        self.assertEqual(response.status_code, 200)

    def test_question_list(self):
        questions = {}
        count = 10
        for i in range(count):
            questions[i] = RandomQuestionFactory.create()

        response = self.client.get('/questions/')
        content = json.loads(response.content)

        self.assertEqual(Question.objects.all().count() - 1, count)
        for i in range(count):
            self.assertEqual((self.client.get('/questions/{}/detail/'.format(questions[i].pk))).status_code, 200)

        self.assertEqual(response.status_code, 200)





class RandomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'test_{}_login'.format(n))
    email = factory.Sequence(lambda n: 'test_{}_email@test.test'.format(n))


class RandomQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    name = factory.Sequence(lambda n: 'test_{}_question'.format(n))
    data = factory.Sequence(lambda n: 'Data of the quest_{}'.format(n))
    author = factory.SubFactory(RandomUserFactory)