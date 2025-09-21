from django.urls import path
from . import views

urlpatterns = [

    path('form/', views.teamform, name='team'),
    path('', views.homeawayview, name='select_week'),
    path('final/', views.print_final, name='final'),
    path('winner/', views.winnerPick, name='winner'),
    path('total/',views.total, name='total'),
    path('winners/', views.print_winners,name='print_winners'),
    #path('winner1/',views.winnerPick1,name='winner1'),
    path('print_week/',views.print_week,name='week'), # Added 7/7/2023 - lets get the player and total points and the week to print.
    path('<int:week_number>/',views.printWeek, name='print_week'),# Print this weeks schedule.
    path('confirm_selections/',views.confirm_selections, name='confirm_selections'),
    path('pick_week/',views.pick_week,name='pick_week'),
    path('update/<int:id>/', views.update, name='update'),
    #path('pick_week/pick_year/',views.pick_week_year, name = 'pick_week_year'),
    path('select_winners/',views.select_winners,name='select_winners'),
    path('save_winners/',views.save_winners,name='save_winners'),
    path('week/',views.winner_select_view, name='winner_select'),
    path('list/', views.winnerPickList, name='list'),
    path('list_id/', views.winnerPickList_id, name='list_id'),
    path('winnerPickNew/<int:id>/', views.winnerPickNew, name='winnerPickNew'),
    path('teamNew/', views.teamNew, name='teamNew'),
    path('delete/<int:id>/',views.delete, name='delete'),
    path('scores/<int:id>/',views.scores, name='scores'),
    path('scoresNew/',views.scoresNew, name='scoresNew'),   # Added 08/08/2025
    path('list_week/', views.winnerPickListWeek, name='list_week'),
    path('totalWins/', views.totalWins, name = 'totalWins'),
    path('weeklyTotals/', views.weeklyTotals, name='weeklyTotals'),
]
