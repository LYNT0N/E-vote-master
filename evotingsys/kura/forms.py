from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django import forms
from .models import Candidate


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'year_of_study','faculty','Position']

