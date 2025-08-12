from django.shortcuts import render, redirect
from . forms import HomeAwayForm, TeamForm, WinnerPickForm,WinnerSelectForm
from .models import Team, Home_Away,WinnerPick
from players import PLAYERS,Players # Players in the pool
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#--------- Add a new Team.------------------------------
def teamform(request):
    '''
    '''
    form = TeamForm(request.POST or None)
            
    if form.is_valid():
        form.save()

        form = TeamForm()
    return render(request, 'teams/team.html', {'form': form})

#---------End of add a new Team--------------------------
# My home page.
def homeawayview(request):
    '''
    '''
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

def homeawaylist(request):
    '''
    '''
    games = Home_Away.objects.all().order_by('id',)
    context = {
        'games':games
    }
    return render(request, 'teams/home_away_list.html', context)

def print_final(request):
    '''
    '''
    winners=WinnerPick.objects.all()
    context = {
        "winners":winners,
        "players":PLAYERS
    }
    return render(request, 'teams/final.html',context)


def winnerPick(request):  # Lets select the winner from a particular week
    '''
    '''
    if request.method == ('POST' or None):
        form = WinnerPickForm(request.POST)                                    
        if form.is_valid():
            week_number=form.cleaned_data['week_number']
            print(week_number)
            form.save()
            return redirect('list')
    else:
        form=WinnerPickForm()
    context={
        "form":form,
       
    }
    return render(request,'teams/select_your_picks.html', context)

def print_winners(request):
    '''
    '''
    return render(request, 'teams/print_winners.html')

def printWeek(request,week_number  ):  # We also need to check the year.
    '''
    '''    
    home_aways = Home_Away.objects.filter(week_number=week_number).order_by('startdate','starttime')
    total=home_aways.count()
    context = {
        'home_aways':home_aways,
        'week_number':week_number,
        'total':total       
    } 
    return render (request,'teams/print_week.html', context)


def select_winners(request):
    '''
    '''
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
    '''
    '''
    week_number=request.GET.get('week_number')
    home_aways = Home_Away.objects.filter(week_number=week_number).order_by('startdate','starttime')
    
    context = {
        'home_aways':home_aways,
        'week_number':week_number,
    } 
    return render (request,'teams/print_week.html', context)



def confirm_selections(request):
    '''
    List our selections from HomeAway and show an option 
    to edit my choices.
    '''
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
    '''
    '''
    context = {
        "players":Players,
    }
    return render(request,'teams/pick_week.html', context)

def save_winners(request):
    '''
    '''
    pick=request.GET.get('8')
    print('pick',pick)
    context={
        "pick":pick,

    }
    return render(request, 'teams/winners_saved.html',context)

@login_required
def winner_select_view(request):
    '''
    '''
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

def update(request, id):
    '''
    '''
    entry = WinnerPick.objects.get(id=id)
    
    if request.method != 'POST':
        form = WinnerPickForm(instance = entry)
    else:
        form = WinnerPickForm(instance=entry, data=request.POST)
        if form.is_valid():
           form.save()
        return redirect('list')        
    context = {

        'entry':entry,
        'form':form,
    }
    return render(request,'teams/winnerPickUpdate.html',context )

def winnerPickNew(request, id):
    '''
    Take the HomeAway to get year, home, away, week_number to add to
    the winner pick choices.
    '''
    if request.method ==('POST' or None):
        week_number   = request.GET['week_number']
        #year          = request.GET['year']
        #year          = '2025'
        player        = request.GET['player']
        away          = request.GET['away']
        home          = request.GET['home']
        away_score    = request.GET['away_score']
        home_score    = request.GET['home_score']
        actual_winner = request.GET['actual_winner']
        status        = request.GET['status']
        WinnerPick.objects.create(week_number=week_number,year=year,player=player,away=away,home=home,away_score=away_score,home_score=home_score,actual_winner=actual_winner,status=status)
        return redirect('list')
    else:
        selection   = Home_Away.objects.get(id = id)
        week_number = selection.week_number
        away   = selection.away_team
        home   = selection.home_team
        year        = 2025
        player      = 'Mom'
        
    print(week_number, away,home)
     
    form = WinnerPickForm({week_number:week_number,year:year,away:away, home:home  })
    print(form)
    context = {
        'form':form,
    }
    return render(request, 'teams/select_your_picks.html', context)
    
    
def winnerPickList(request):
    '''
    '''
    list=WinnerPick.objects.all().order_by('-id',)
    p= Paginator(list,16)
    page_number = request.GET.get('page')
    page= request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, then assign the first page.
        page_obj =p.page()    
    except EmptyPage:
        # If page is empty then return last page.
        page_obj = p.page(p.num_pages)
    page_obj = p.get_page(page)        
    
    context = {
        #'list':list,
        'page_obj':page_obj,
    }
    return render(request, 'teams/winnerPickList.html', context)
    #return render(request, 'teams/paginator.html', context)       # This is a paginator setup

def print_player_week_selections(request):
    '''
    '''
    form =WinnerPickForm()
    if request.method=='POST':
        week_number = request.POST['week_number']
        year        = request.POST['year']
        player      = request.POST['player']
        winners     = WinnerPick.objects.filter(week_number__icontains=week_number).filter(year__icontains=year).filter(player__icontains=player)
        
        context={
            'winners':winners,
            #'iterater':range(0,10),
        }    
        return render(request,'teams/print_selected_winners.html', context)    
    context ={
        'form':form,
        'players':Players,
        #'winners':winners    
    }
    return render(request,'teams/print_player_week_selections.html', context)

def pick_winner_list(request):
    '''
    '''
    week_number=request.GET.get('week_number')
    year = request.GET.get('year') 
    player = request.GET.get('player')
    paginate_by = 16
    
    context={
        'week_number':week_number,
        'year'       :year,
        'players'     :Players,
        
    }    
    return render(request,'teams/print_player_week_selections.html',context)

def delete(request, id):
    '''
    '''
    success=''
    winner=WinnerPick.objects.get(id=id)
    winner.delete()
    success='You have deleted the winner.'
    context = {
        'success':success,
    }
    return render(request, 'teams/delete.html',context)

def games(request):
    '''
    '''
    games=Home_Away.objects.all().order_by('id', 'week_number','startdate', 'starttime')
    context = {
        'games':games,
    }
    return render(request, 'teams/home_away.html',context)   

def scores(request,id):
    '''
    '''
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
        ual_winner = 'Tie'
                
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

def total(request):
    '''
    The Total number of wins per week for each player. 
    '''
    results = []   # This hold the player and the total wins
    for week_number  in range (1, 19):
        for player in Players:
    
            # Total number of wins in week_number for that particular player. 
            total=WinnerPick.objects.filter(week_number=week_number).filter(player = player).filter(status='Win')
            total = len(total)
            if total == 1: 
                results.append(week_number)
                results.append(player)
                results.append(total)
                print(results) 
                #results.append(f'{player} has won {total}  game in week number {week_number}.')
            elif total > 1:    
                results.append(week_number)
                results.append(player)
                results.append(total)
                #results.append(f'{player} has won {total}  games in week number {week_number}.')
                            
    context={
        'results':results,
        
    }        
    return render(request, 'teams/total.html', context)        
        
def scoresNew(request):
    '''
    '''
    if request.method != 'POST':
        form = WinnerPickForm()
    else:
        form = WinnerPickForm(request.POST)
        if form.is_valid():
           form.save()
        return redirect('list')        
    context = {

        
        'form':form,
    }
    return render(request,'teams/winnerPickUpdate.html',context )

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
    
def total(request):
    '''
    The Total number of wins per week for each player. 
    '''
    print('function total called')
    results = []   # This hold the player and the total wins
    for week_number  in range (1, 19):
        
        
        for player in Players:
             
            # Total number of wins in week_number for that particular player. 
            total=WinnerPick.objects.filter(week_number=week_number).filter(player = player).filter(status='Win').count()
            
            
            if total >= 1: 
                results.append(f'{player} has won {total} game(s) in week number {week_number}.')
                #results.append(week_number)
                #results.append(total)
                
                
                #results.append(f'{player} has won {total}  game in week number {week_number}.')
    print(results)            
                            
    context={
        'results':results,
        
    }        
    return render(request, 'teams/total.html', context)        
        