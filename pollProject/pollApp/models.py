from django.contrib.auth.models import User
from django.db import models
# Question class
class Question(models.Model):
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    voted_users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.choice_text

class Voters(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Initially allow null
    admission_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    voted_questions = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return self.name
