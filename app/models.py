from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
	content = models.CharField(max_length=3000)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	upvotes = models.PositiveIntegerField(default=0)
	downvotes = models.PositiveIntegerField(default=0)

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	content = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	upvotes = models.PositiveIntegerField(default=0)
	downvotes = models.PositiveIntegerField(default=0)
