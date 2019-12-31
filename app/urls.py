
"""quora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *
from .api import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('ask/', login_required(CreateQuestion.as_view()), name='ask'),
    path('question/<int:pk>/view/', ViewQuestion.as_view(), name='question-view'),
    path('question/<int:pk>/edit/', login_required(UpdateQuestion.as_view()), name='question-edit'),
    path('question/<int:pk>/delete/', login_required(DeleteQuestion.as_view()), name='question-delete'),
    path('question/<int:pk>/answer/', login_required(CreateAnswer.as_view()), name='answer'),
    path('answer/<int:pk>/edit/', login_required(UpdateAnswer.as_view()), name='answer-edit'),
    path('answer/<int:pk>/delete/', login_required(DeleteAnswer.as_view()), name='answer-delete'),
    path('answer/<int:pk>/comment/', login_required(CreateComment.as_view()), name='comment'),
    path('comment/<int:pk>/edit/', login_required(UpdateComment.as_view()), name='comment-edit'),
    path('comment/<int:pk>/delete/', login_required(DeleteComment.as_view()), name='comment-delete'),
    path('vote/', VoteAPI.as_view(), name='vote'),
    path('search/', Search.as_view(), name='search')
]
