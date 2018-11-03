# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client

from core.models import User



class TestQuestion(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user', email='test_email')
        self.user.set_password('test_password')
        self.user.save()

        self.client = Client()

    def test_core_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_core_profile(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_core_register(self):
        self.client.logout()
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

