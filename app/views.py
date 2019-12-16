from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Question, Answer

class Home(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Home, self).get_context_data(*args, **kwargs)
		context['questions'] = Question.objects.all()
		return context


class CreateQuestion(CreateView):
	model = Question
	fields = ('content',)
	success_url = '/'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(CreateQuestion, self).form_valid(form)


class ViewQuestion(TemplateView):
	template_name = "question_view.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ViewQuestion, self).get_context_data(*args, **kwargs)
		context['question'] = Question.objects.get(pk=self.kwargs.get('pk'))
		return context


class UpdateAnswer(UpdateView):
	model = Answer
	fields = ('content',)

	def get_success_url(self):
		pk = self.kwargs['pk']
		question = Answer.objects.get(pk=self.kwargs.get('pk')).question
		success_url = reverse_lazy('question-view', kwargs={'pk':question.pk})
		return success_url

	def get_context_data(self, *args, **kwargs):
		context = super(UpdateAnswer, self).get_context_data(*args, **kwargs)
		context['question'] = Answer.objects.get(pk=self.kwargs.get('pk')).question
		return context


class CreateAnswer(CreateView):
	model = Answer
	fields = ('content',)

	def get_success_url(self):
		pk = self.kwargs['pk']
		success_url = reverse_lazy('question-view', kwargs={'pk':pk})
		return success_url

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.question = Question.objects.get(pk=self.kwargs.get('pk'))
		return super(CreateAnswer, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(CreateAnswer, self).get_context_data(*args, **kwargs)
		context['question'] = Question.objects.get(pk=self.kwargs.get('pk'))
		return context
