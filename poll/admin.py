from django.contrib import admin

from poll.models import *


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = list_display


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text','poll')
    list_display_links = list_display


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'grade', 'question_lead_to')
    list_display_links = list_display


@admin.register(AnswerGiven)
class AnswerGivenAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question_text', 'poll',)
    list_display_links = list_display