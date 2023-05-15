from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=200)

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Position(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Candidate(models.Model):
    name = models.CharField(max_length=200)
    Position = models.ForeignKey(Position, on_delete=models.CASCADE,related_name='candidate_set')
    year_of_study = models.PositiveSmallIntegerField(default=1)
    faculty = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.voter_id = self.user.username + '_' + str(self.user.id)
        super(Voter, self).save(*args, **kwargs)    

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'position')
