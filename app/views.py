from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse

from .models import Question, Answer, Vote, Comment


class BaseUpdateView(UpdateView):
	def dispatch(self, request, *args, **kwargs):
		""" Hook to ensure object is owned by request.user """
		obj = self.get_object()
		if obj.author != self.request.user:
			return HttpResponse("You are not allowed to edit this Post", status=401)
		return super(BaseUpdateView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.updated_at = timezone.now()
		return super(BaseUpdateView, self).form_valid(form)


class BaseDeleteView(DeleteView):
	success_url = reverse_lazy('home')
	template_name = 'app/confirm_delete.html'

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, "Deleted successfully")
		return super(BaseDeleteView, self).delete(request, *args, **kwargs)

	def get_object(self, queryset=None):
		""" Hook to ensure object is owned by request.user """
		obj = super(BaseDeleteView, self).get_object()
		if not obj.author == self.request.user:
			return HttpResponse("You are not allowed to edit this Post", status=401)
		return obj


class Home(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Home, self).get_context_data(*args, **kwargs)
		context['questions'] = Question.objects.all()
		return context


class CreateQuestion(CreateView):
	model = Question
	fields = ('content',)
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(CreateQuestion, self).form_valid(form)


class UpdateQuestion(BaseUpdateView):
	model = Question
	fields = ('content',)

	def get_success_url(self):
		return reverse_lazy('question-view', kwargs={'pk':self.kwargs.get('pk')})

	def get_context_data(self, *args, **kwargs):
		context = super(UpdateQuestion, self).get_context_data(*args, **kwargs)
		context['question'] = self.get_object()
		return context


class ViewQuestion(TemplateView):
	template_name = "question_view.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ViewQuestion, self).get_context_data(*args, **kwargs)
		pk = self.kwargs.get('pk')
		context['question'] = Question.objects.get(pk=pk)
		return context


class DeleteQuestion(BaseDeleteView):
	model = Question


class CreateAnswer(CreateView):
	model = Answer
	fields = ('content',)

	def get_success_url(self):
		pk = self.kwargs['pk']
		success_url = reverse_lazy('question-view', kwargs={'pk':pk})
		return success_url

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.for_question = Question.objects.get(pk=self.kwargs.get('pk'))
		return super(CreateAnswer, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(CreateAnswer, self).get_context_data(*args, **kwargs)
		context['question'] = Question.objects.get(pk=self.kwargs.get('pk'))
		return context


class UpdateAnswer(BaseUpdateView):
	model = Answer
	fields = ('content',)

	def get_success_url(self):
		question = Answer.objects.get(pk=self.kwargs.get('pk')).for_question
		success_url = reverse_lazy('question-view', kwargs={'pk':question.pk})
		return success_url

	def get_context_data(self, *args, **kwargs):
		context = super(UpdateAnswer, self).get_context_data(*args, **kwargs)
		context['question'] = self.get_object().for_question
		return context


class DeleteAnswer(BaseDeleteView):
	model = Answer


class CreateComment(CreateView):
	model = Comment
	fields = ('content',)

	def get_success_url(self):
		answer = Answer.objects.get(pk=self.kwargs.get('pk'))
		success_url = reverse_lazy('question-view', kwargs={'pk':answer.for_question.pk})
		return success_url

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.for_answer = Answer.objects.get(pk=self.kwargs.get('pk'))
		return super(CreateComment, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(CreateComment, self).get_context_data(*args, **kwargs)
		context['answer'] = Answer.objects.get(pk=self.kwargs.get('pk'))
		return context


class UpdateComment(BaseUpdateView):
	model = Comment
	fields = ('content',)

	def get_success_url(self):
		answer = Comment.objects.get(pk=self.kwargs.get('pk')).for_answer
		success_url = reverse_lazy('question-view', kwargs={'pk':answer.for_question.pk})
		return success_url

	def get_context_data(self, *args, **kwargs):
		context = super(UpdateComment, self).get_context_data(*args, **kwargs)
		context['answer'] = self.get_object().for_answer
		return context


class DeleteComment(BaseDeleteView):
	model = Comment


class Search(TemplateView):
	template_name='search.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Search, self).get_context_data(*args, **kwargs)
		query = self.request.GET['query']
		context.update({
			'query': query,
			'results': Question.objects.filter(content__icontains=query)
		})
		return context