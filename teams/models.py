from email.policy import default
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
#team=Home_Away.objects.first()
from teams1 import TEAMS 
from players import PLAYERS
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Add a new team 
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Home_Away(models.Model):
    
    
    week_number = models.IntegerField(blank=False, null=False)
    
    away_team = models.CharField(max_length=100, choices=TEAMS, default='')
    home_team = models.CharField(max_length=100, choices=TEAMS, default='')
   
    startdate = models.DateField(
        editable=True, null=True, blank=True)
    starttime = models.TimeField(editable=True, null=True, blank=True)

    class Meta:
        ordering = ['week_number','startdate','home_team' ]

    def __str__(self):
        return f'{ self.home_team} and { self.away_team }'
    
    
    
STATUS = [
    ("Win","Win"),
    ("Lose","Lose"),
    ("Tie", "Tie")
]

PICK =[
    ('Away','Away'),
    ('Home','Home'),
]
class WinnerPick(models.Model):
    week_number  = models.IntegerField(null=True )
    year = models.PositiveSmallIntegerField(default=2025)
    player       = models.CharField(max_length=200, choices=PLAYERS, default='Mr C',null=True)
    away = models.CharField(max_length=200, choices =TEAMS, null= True )
    home = models.CharField(max_length=200, choices =TEAMS, null= True )
    away_score = models.PositiveSmallIntegerField(null = True, default=0)    
    home_score = models.PositiveSmallIntegerField(null = True, default=0)
    selected_pick  = models.CharField(max_length=250, choices=PICK, null = True)
    actual_winner = models.CharField(max_length=250,  choices=PICK, null = True)
    status = models.CharField(max_length=6, null=True, choices=STATUS)
    
    class Meta:
        ordering = ['player', 'week_number'] 

    def __str__(self):
        return self.selected_pick    
@login_required    
class WinnerSelect(models.Model):
    player=models.ForeignKey(User,on_delete=models.CASCADE)
    week_number = models.IntegerField()
    selected_team= models.CharField(max_length=200)

    def __str__(self):
        return self.selected_team


