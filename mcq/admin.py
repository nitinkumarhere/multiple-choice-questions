# -*- coding: utf-8 -*-s
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import QuestionPaper, Question, Choice, Candidate, Submission


admin.site.register(Question)

admin.site.register(QuestionPaper)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Candidate)