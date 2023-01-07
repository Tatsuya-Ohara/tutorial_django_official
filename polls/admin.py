from django.contrib import admin
from .models import Question

# adminにQuestionを表示する
admin.site.register(Question)