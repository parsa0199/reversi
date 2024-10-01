from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from .models import Game
from django.urls import reverse_lazy

# List all games
class GameListView(ListView):
    model = Game
    template_name = 'game/game_list.html'
    context_object_name = 'games'

# Start a new game
class GameCreateView(CreateView):
    model = Game
    fields = ['player1', 'player2', 'current_turn']  # Fields to fill when creating a game
    template_name = 'game/game_form.html'
    success_url = reverse_lazy('game:game_list')

# View details of a specific game
class GameDetailView(DetailView):
    model = Game
    template_name = 'game/game_detail.html'

# View for playing the game
class GamePlayView(DetailView):
    model = Game
    template_name = 'game/play_game.html'

    # Here, you'd add logic for handling the game's turn-based interaction
