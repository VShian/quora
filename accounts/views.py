from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy, reverse
from app.views import Question, Answer


class CreateUser(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('profile-update')


class UpdateProfile(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('profile')

    def get_form(self, form_class=None):
        form = super(UpdateProfile, self).get_form(form_class)
        for field in self.fields:
            form.fields[field].required = True
        return form

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateProfile, self).get_context_data(*args, **kwargs)
        context['login_link'] = False
        return context


class Profile(TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Profile, self).get_context_data(*args, **kwargs)
        context.update({
            'profile': self.request.user,
            'questions': Question.objects.filter(author=self.request.user),
            'answers': Answer.objects.filter(author=self.request.user)
        })
        return context


class AnonProfile(TemplateView):
    template_name = 'registration/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.username == self.kwargs.get('username'):
            return redirect('profile')

        return super(AnonProfile, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AnonProfile, self).get_context_data(*args, **kwargs)
        profile = get_object_or_404(User, username=self.kwargs.get('username'))
        context.update({
            'profile': profile,
            'questions': Question.objects.filter(author=profile),
            'answers': Answer.objects.filter(author=profile)
        })
        return context


class PasswordChange(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('logout')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed successfully.')
        return super().form_valid(form)



