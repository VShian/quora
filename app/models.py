from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Base(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Question(Base):
	content = models.CharField(max_length=3000)


class Reply(Base):
	content = models.TextField()

	def upvotes(self):
		return self.vote_set.filter(vote_type=Vote.UPVOTE).count()

	def downvotes(self):
		return self.vote_set.filter(vote_type=Vote.DOWNVOTE).count()


class Answer(Reply):
	for_question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Comment(Reply):
	for_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class Vote(models.Model):
	UPVOTE, DOWNVOTE = 0, 1
	VOTE_TYPE = [
		(UPVOTE, "Upvote"),
		(DOWNVOTE, "Downvote"),
	]

	vote_type = models.PositiveIntegerField(choices=VOTE_TYPE)
	reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

