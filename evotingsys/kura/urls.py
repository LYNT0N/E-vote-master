from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_view
from . import views
from kura.views import vote, thank_you

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='kura/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='kura/logout.html'), name="logout"),
    path('add_candidate/', views.add_candidate, name='add_candidate'),
    path('vote/', views.vote, name='vote'),
    path('positions/', views.positions, name='positions'),
    path('poll_detail/', views.poll_detail, name='poll_detail'),
    path('already_voted/', views.already_voted, name='already_voted'),
    path('vote/', vote, name='vote'),
    path('thank-you/', thank_you, name='thank_you'),
    path('results/', views.results, name='results'),
]





 
