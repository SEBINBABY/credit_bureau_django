from rest_framework import serializers
from .models import Question, UserResponse

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'answer_a', 'answer_b', 'answer_c', 'answer_d']