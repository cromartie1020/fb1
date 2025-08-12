from django.shortcuts import render, redirect, HttpResponseRedirect
from . forms import HomeAwayForm, TeamForm, WinnerPickForm,WinnerSelectForm
from .models import Team, Home_Away,WinnerPick
from players import PLAYERS,Players # Players in the pool
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator  

# Add a new Team.
def teamform(request):
    form = TeamForm(request.POST or None)
            
    if form.is_valid():
        form.save()

        form = TeamForm()

    return render(request, 'teams/team.html', {'form': form})
def homeawayview(request):
    
    teams = Team.objects.all()
    form = HomeAwayForm(request.POST or None)
    
    if form.is_valid():
        week_number=request.POST['week_number']
        year = 2025
        home = request.POST['home_team']
        away = request.POST['away_team']
    
        for player in Players:
            
            winner=WinnerPick(week_number=week_number,year=year,player=player,away=away, home=home)
            winner.save()
        form.save()
        form = HomeAwayForm()
        redirect('winner')

    else:
        form = HomeAwayForm()
        

    return render(request, 'teams/select_teams.html', {'form': form, 'teams': teams})


'''
def homeawayview(request):
    teams = Team.objects.all()
    form = HomeAwayForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = HomeAwayForm()
        redirect('winner')

    else:
        form = HomeAwayForm()
        

    return render(request, 'teams/select_teams.html', {'form': form, 'teams': teams})
'''
def print_final(request):
    winners=WinnerPick.objects.all()
    context = {
        "winners":winners,
        "players":PLAYERS
    }
    return render(request, 'teams/final.html',context)
    

def select_your_picks(request):
    pass

def winnerPick(request):  # Lets select the winner from a particular week
    if request.method == ('POST' or None):
        form=WinnerPickForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form=WinnerPickForm()
    context={
        "form":form
    }
    
    return render(request,'teams/select_your_picks.html', context)

def winnerPick1(request):
    if request.method =='GET':
        week_number= request.GET['week_number']
        year = request.GET['year']
        player = request.GET['player']
        form= WinnerPickForm({'week_number':week_number,'year':year,'player':player})
    else:
        form=WinnerPickForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('select_week')
    context={
        'form':form
    }
    return render(request, 'teams/select_your_picks.html', context)
def total(request):
    pass

def print_winners(request):
    return render(request, 'teams/print_winners.html')

def printWeek(request,week_number  ):  # We also need to check the year.
    
    home_aways = Home_Away.objects.filter(week_number=week_number).order_by('startdate','starttime')
    total=home_aways.count()
    
     
    context = {
        'home_aways':home_aways,
        'week_number':week_number,
        'total':total       
       


    } 
    
           

    return render (request,'teams/print_week.html', context)


def select_winners(request):
   
    week_number=request.GET.get('week_number')
    player=request.GET.get('player')
    
    selections=Home_Away.objects.filter(week_number=week_number)
    
    week_number=request.GET.get('week_number')
    home_aways = Home_Away.objects.filter(week_number=week_number).order_by('startdate','starttime')
    total=home_aways.count()
    form=WinnerPickForm()


    context = {
        
        'form':form,
        'week_number':week_number,
        'home_aways':home_aways,
        'total':total,
        
    
    }
    
    
      
    return render(request, 'teams/select_winners.html', context)    

def print_week(request):  # This function added 7/7/2023 to replace printweek function
    week_number=request.GET.get('week_number')
    home_aways = Home_Away.objects.filter(week_number=week_number).order_by('startdate','starttime')
    
    
    
    context = {
        'home_aways':home_aways,
        'week_number':week_number,
         
        


    } 
    
           

    return render (request,'teams/print_week.html', context)



def confirm_selections(request):
    # List our selections from HomeAway and show an option 
    # to edit my choices.
    week_number=request.GET.get('week_number')
    year = request.GET.get('year') 
    #year = request.GET.get((year)
    selections=Home_Away.objects.filter(week_number=week_number)
    week_number=request.GET.get('week_number')
    home_aways = Home_Away.objects.filter(week_number=week_number).filter(startdate__year=year).order_by('startdate','starttime')
    
    # ______Lets find a way to determine the teams on a bye. _____________________________
    #_____________________________________________________________________________________

    context={
        'selections':selections,
        'week_number':week_number,
        'home_aways':home_aways,
        'year':year,
    }
    return render(request, 'teams/print_week.html',context)  

def pick_week(request):
    

    
    context = {
        "players":Players,


    }
    return render(request,'teams/pick_week.html', context)

def winnerPickList(request):
    list=WinnerPick.objects.all().order_by('week_number', 'player')
    
    paginator = Paginator(list, 16)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'teams/winnerPickList.html',{'page_obj':page_obj })

def save_winners(request):
    print('request', request)
    pick=request.GET.get('8')
    print('pick',pick)
    context={
        "pick":pick,

    }
    return render(request, 'teams/winners_saved.html',context)

@login_required
def winner_select_view(request):
    week_number=request.GET.get('week_number')
    print('week_number:',week_number)
    home_aways = Home_Away.objects.filter(week_number=week_number).order_by('startdate','starttime')
    
    
    print ('home_aways:',home_aways)
    #form=WinnerSelectForm()
    context={
        "teams":home_aways,
        #"form":form,

    }


    return render(request,'teams/select_winners.html',context)
def winnerPickNew(request,id):
    list = WinnerPick.objects.get(id=id)
    form = WinnerPickForm(instance=list) 
    
    if request.method==('POST' or None):
        week_number= request.GET['week_number']
        year= request.GET['year']
        player= request.GET['player']
        away= request.GET['away']
        home= request.GET['home']
        away_score= request.GET['away_score']
        home_score= request.GET['home_score']
        actual_winner = request.GET['actual_winner']
        status = request.Get['status']
        winner=WinnerPick(week_number=week_number,year=year,player=player, away=away,home=home,away_score=away_score,home_score=home_score,actual_winner=actual_winner,status=status)
        winner.save()
        
        return render('list')
        
    
    context={
        'form':form,
    }
    return render(request, 'teams/select_your_picks.html', context)     
    

def update(request, id):
    list = WinnerPick.objects.get(id=id)
    
    
    if request.method == ('POST' or None):
        form = WinnerPickForm(request.POST, instance = list)
        if form.is_valid():
            
            form.save()
            return redirect('list')
    else:
        form = WinnerPickForm(instance =  list)
    context = {
        'form':form,
        #'list':list
    }    

    return render(request, 'teams/winnerPickUpdate.html', context)

def teamNew(request):
    form = TeamForm()
    if request.method == ('POST' or None):
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    context = {
        'form':form
    }      
    return render(request, 'teams/teamNew.html', context)

def delete(request, id):
    winner = WinnerPick.objects.get(id=id)
    winner.delete()
    context={
        'success':'The winner item has been successfully deleted.',
    }
    return render(request, 'teams/delete.html', context)



def scores(request,id):
    
    global temp
    temp = id
    #Update the scores with each player
    #Input the selected winner.
    winners=WinnerPick.objects.all()
    
    
    list = WinnerPick.objects.get(id = id)
    week_number = list.week_number
    year = list.year
    player = list.player 
    away = list.away
    home = list.home
    away_score = list.away_score
    home_score = list.home_score
    selected_pick = list.selected_pick
    actual_winner = list.actual_winner
    status = list.status
     
    instance = list
    #print('list: ', list)
    WinnerPickForm(instance = list)
    
    if request.method == ('POST' or None):
        week_number   = request.POST['week_number']
        year          = request.POST['year']
        player        = request.POST['player']
        away          = request.POST['away']
        home          = request.POST['home']
        away_score    = request.POST['away_score']
        home_score    = request.POST['home_score']
        home_score    = int(home_score)
        away_score    = int(away_score)
        week_number   = int(week_number)
        selected_pick = request.POST['selected_pick']
        
        if home_score    > away_score:
            actual_winner = home
        if away_score    > home_score:
            actual_winner = away
            
        if actual_winner == selected_pick:
            status = 'Win'    
        if actual_winner != selected_pick:
            status = 'Loss'    
            
        if home_score == away_score:
            actual_winner = 'Tie'
            status        = 'Tie'    
        '''
        print('actual_winner: ',actual_winner)         
        if (home_score > away_score) and (selected_pick == home):
            status = 'Win'    
        if (away_score > home_score) and (selected_pick == home):
            status = 'Loss'    
        if away_score == home_score:
            status = 'Tie'
            actual_winner = 'Tie'
        '''        
        form = WinnerPick( week_number=week_number, year=year, player=player, away= away, home=home, away_score=away_score, home_score=home_score, selected_pick=selected_pick,actual_winner=actual_winner, status=status)
        
        form.save()
        winner = WinnerPick.objects.get(id=temp)
        winner.delete()
        return redirect('list')
        
    context = {
        'week_number':week_number,
        'year':2025,
        'player':player,
        'away':away,
        'home':home,
        'away_score':away_score,
        'home_score':home_score,
        'selected_pick':selected_pick,
        'actual_winner':actual_winner,
        'status':status,
    }
    return render(request, 'teams/winnerPickUp.html', context)
