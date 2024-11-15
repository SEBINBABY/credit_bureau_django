from django.contrib import admin
from .models import Question, UserResponse, UserScore

# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_text', 'answer_a', 'answer_b', 'answer_c', 'answer_d']
    list_per_page = 10
    search_fields = ['question_text']

admin.site.register(UserResponse)
admin.site.register(UserScore)

