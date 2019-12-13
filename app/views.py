from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Question

class Home(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Home, self).get_context_data(*args, **kwargs)
		context['questions'] = Question.objects.all()
		return context
