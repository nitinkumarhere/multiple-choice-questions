# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Question(models.Model):
    text = models.CharField(max_length= 200)

    def __unicode__(self):
        return self.text

class QuestionPaper(models.Model):
    title = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question, related_name='papers')

    def __unicode__(self):
        return self.title


class Choice(models.Model):
    text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, related_name='choices')
    is_answer = models.BooleanField(default=False)

    def __unicode__(self):
        return self.text


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Submission(models.Model):
    candidate = models.ForeignKey(Candidate)
    question_paper = models.ForeignKey(QuestionPaper)
    choices = models.ManyToManyField(Choice)


    def __unicode__(self):
        return "%s - %s" % (self.candidate.user.username, self.question_paper.title)

    class Meta:
        unique_together = (('candidate', 'question_paper'),)











