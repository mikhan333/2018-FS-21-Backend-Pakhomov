# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from core.models import User
from .models import Category
from questions.models import Question

import json, factory, mock
from mock import patch


class TestQuestion(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user', email='test_email')
        self.user.set_password('test_password')
        self.user.save()

        self.client = Client()

        self.category = Category.objects.create(name='test_category')
        #self.category = Category.objects.create(name='test_category')

    def test_category_detail_login(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get('/categories/{}/'.format(self.category.pk))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_logout(self):
        self.client.logout()
        response = self.client.get('/categories/{}/'.format(self.category.pk))
        self.assertEqual(response.status_code, 200)

    def test_category_list(self):
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)