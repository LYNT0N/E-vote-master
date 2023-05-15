from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from kura import forms
from .models import Poll, Choice,Position,Candidate,Vote
from .forms import CandidateForm
from django.core.mail import send_mail
from .models import Voter
from django.db.models import Count


def home(request):
    return render(request, 'kura/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'kura/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'kura/profile.html')

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'kura/poll_detail.html', {'poll': poll})

@login_required
def vote(request):
    if request.method == 'POST':
        # Get the selected candidates for each position
        selected_candidates = {}
        for position_id in request.POST:
            if position_id.startswith('position_'):
                candidate_id = request.POST.get(position_id)
                if candidate_id:
                    selected_candidates[int(position_id.replace('position_', ''))] = int(candidate_id)

        # Check if the user has already voted for any of the selected positions
        user = request.user
        for position_id, candidate_id in selected_candidates.items():
            position = Position.objects.get(pk=position_id)
            candidate = Candidate.objects.get(pk=candidate_id)
            if Vote.objects.filter(user=user, position=position).exists():
                return render(request, 'kura/already_voted.html')

        # Create a new vote object for the user for each selected position
        for position_id, candidate_id in selected_candidates.items():
            position = Position.objects.get(pk=position_id)
            candidate = Candidate.objects.get(pk=candidate_id)
            vote = Vote.objects.create(user=user, candidate=candidate, position=position)
            vote.save()

        return redirect('thank_you')

    positions = Position.objects.all()
    candidates = Candidate.objects.all()
    context = {'positions': positions, 'candidates': candidates}
    return render(request, 'kura/vote.html', context)


def add_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CandidateForm()
    return render(request, 'kura/add_candidate.html', {'form': form})

@login_required
def register_voter(request):
    voter = Voter.objects.create(user=request.user)
    subject = 'Your voter ID'
    message = 'Your voter ID is: ' + voter.voter_id
    recipient_list = [request.user.email]
    send_mail(subject, message, 'sender@example.com', recipient_list)
    return redirect('home')    

def positions(request):
    positions = Position.objects.all()
    candidates = Candidate.objects.all()
    context = {'positions': positions, 'candidates': candidates}
    return render(request, 'positions.html', context)

def already_voted(request):
    return render(request, 'kura/already_voted.html')

def thank_you(request):
    return render(request, 'kura/thank_you.html' )

from django.db.models import Count

def results(request):
    positions = Position.objects.all()
    results = []
    
    for position in positions:
        candidates = Candidate.objects.filter(Position=position)
        position_results = []
        
        for candidate in candidates:
            votes = Vote.objects.filter(position=position, candidate=candidate).count()
            position_results.append((candidate, votes))
        
        # Sort position_results based on the vote count in descending order
        position_results.sort(key=lambda x: x[1], reverse=True)
        
        # Get the winner (candidate with the highest votes)
        winner = position_results[0][0] if position_results else None
        
        results.append((position, position_results, winner))
    
    return render(request, 'kura/results.html', {'results': results})




