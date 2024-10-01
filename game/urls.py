from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.GameListView.as_view(), name='game_list'),  # List all games
    path('new/', views.GameCreateView.as_view(), name='new_game'),  # Start a new game
    path('<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),  # View a specific game
    path('<int:pk>/play/', views.GamePlayView.as_view(), name='play_game'),  # Play the game
]
