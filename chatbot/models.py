from django.db import models


class ChatbotQuestion(models.Model):
	question = models.TextField()
	normalized_question = models.CharField(max_length=500, unique=True)
	answer = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	answered_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ('-updated_at',)

	def __str__(self):
		return self.question[:80]
