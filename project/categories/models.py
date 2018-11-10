# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class CategoryQuerySet(models.QuerySet):
    pass

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Название категории')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CategoryQuerySet.as_manager()

    class Meta:
        verbose_name=u'Категория'
        verbose_name_plural=u'Категории'
        ordering='name', 'id'
    def __unicode__(self):
        return self.name
