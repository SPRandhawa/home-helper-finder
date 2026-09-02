from django.contrib import admin

from .models import ChatbotQuestion


@admin.register(ChatbotQuestion)
class ChatbotQuestionAdmin(admin.ModelAdmin):
	list_display = ('question', 'answer_status', 'created_at', 'updated_at')
	list_filter = ('answered_at',)
	search_fields = ('question', 'answer')
	readonly_fields = ('normalized_question', 'created_at', 'updated_at', 'answered_at')

	@admin.display(description='Status')
	def answer_status(self, obj):
		return 'Answered' if obj.answer else 'Needs answer'

	def save_model(self, request, obj, form, change):
		from django.utils import timezone

		obj.answered_at = timezone.now() if obj.answer.strip() else None
		super().save_model(request, obj, form, change)
