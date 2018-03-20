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
        blank=True,
        related_name='questions',
        verbose_name=u'Категории'
    )
    is_archive = models.BooleanField(default=False, verbose_name=u'Блок в архиве')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name=u'Вопрос'
        verbose_name_plural=u'Вопросы'
        ordering='name', 'id'

    def __unicode__(self):
        return self.name
