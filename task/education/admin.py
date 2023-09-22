from django.contrib import admin

from education.models import Lesson, LessonView

admin.site.register(Lesson)
admin.site.register(LessonView)

