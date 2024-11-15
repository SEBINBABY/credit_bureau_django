from django.db import models

from django.contrib.auth.models import User  # Import Django's built-in User model

class Question(models.Model):
    # Define the question text
    question_text = models.CharField(max_length=255)   
    # Define possible answers
    answer_a = models.CharField(max_length=255)
    score_a = models.IntegerField(default=0)  # Score for answer A
    answer_b = models.CharField(max_length=255)
    score_b = models.IntegerField(default=0)  # Score for answer B
    answer_c = models.CharField(max_length=255)
    score_c = models.IntegerField(default=0)  # Score for answer C
    answer_d = models.CharField(max_length=255)
    score_d = models.IntegerField(default=0)  # Score for answer D

    def get_score(self, selected_answer):
       # Check which answer was selected and return the corresponding score
        if selected_answer == self.answer_a:
            return self.score_a
        elif selected_answer == self.answer_b:
            return self.score_b
        elif selected_answer == self.answer_c:
            return self.score_c
        elif selected_answer == self.answer_d:
            return self.score_d
        return 0  # Default score if the answer is not valid

    def __str__(self):
        return self.question_text

class UserResponse(models.Model):
    # Link each response to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    # Link each response to a question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Store user's answer
    selected_answer = models.CharField(max_length=255)
    # Track the timestamp of the response
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text} - {self.selected_answer}"

class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)  # Stores the total score of the user

    def __str__(self):
        return f"{self.user.username}'s Score: {self.score}"
