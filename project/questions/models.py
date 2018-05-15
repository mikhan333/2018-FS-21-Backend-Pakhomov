# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Question(models.Model):
    name=models.CharField(max_length=255, verbose_name=u'Название вопроса')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='questions',
        verbose_name=u'Автор'
    )
    categories = models.ManyToManyField(
        'categories.Category',
        blank=False,
        related_name='questions',
        verbose_name=u'Категории'
    )
    is_archive = models.BooleanField(default=False, verbose_name=u'Блок в архиве')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    data = models.TextField(verbose_name=u'Содержимое вопроса')

    class Meta:
        verbose_name=u'Вопрос'
        verbose_name_plural=u'Вопросы'
        ordering='name', 'id'

    def __unicode__(self):

        return self.name

class Like(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='likes',
        verbose_name=u'Like'
    )
    questions = models.ForeignKey(
        'questions.Question',
        related_name='likes',
        verbose_name=u'Likes'
    )
    class Meta:
        verbose_name = u'Лайк'
        verbose_name_plural = u'Лайки'

    def __unicode__(self):
        return self.name


class Answer(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Название ответа')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='answers',
        verbose_name=u'Автор'
    )
    answers = models.ForeignKey(
        'questions.Question',
        related_name='answers',
        verbose_name=u'Ответы'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    data = models.TextField(verbose_name=u'Содержимое ответа', )

    class Meta:
        verbose_name = u'Ответ'
        verbose_name_plural = u'Ответы'
        ordering = 'name', 'id'

    def __unicode__(self):
        return self.name