# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class QuestionQuerySet(models.QuerySet):
    def annotate_manager(self):
        qs = self.select_related('author')
        qs = qs.prefetch_related('categories')
        qs = qs.annotate(likes_count=models.Count('likes', distinct=True),
                         answers_count=models.Count('answers', distinct=True))
        return qs

    def filt_del(self, autho):
        if autho.is_authenticated():
            return self.filter(models.Q(author=autho) | models.Q(is_archive=False))
        else:
            return self.filter(models.Q(is_archive=False))

    def get_stats(self):
        return self.aggregate(likes_count=models.Count('likes', distinct=True),
                              answers_count=models.Count('answers', distinct=True))


class QuestionFile(models.Model):
    file_mime = models.CharField(max_length=72)
    file_key = models.CharField(max_length=72)
    file_content = models.FileField(null = True, upload_to="files")

class Question(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Название вопроса')
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

    photo = models.FileField(null=True, upload_to="photos")
    files = models.ManyToManyField( QuestionFile)

    objects = QuestionQuerySet.as_manager()

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