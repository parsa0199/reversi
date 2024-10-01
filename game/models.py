from django.db import models
from accounts.models import User

# Use the new JSONField from django.db.models
from django.db.models import JSONField

class Game(models.Model):
    player1 = models.ForeignKey(User, related_name='games_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='games_as_player2', on_delete=models.CASCADE)
    board_state = JSONField(default=dict)  # Use django.db.models.JSONField
    current_turn = models.CharField(max_length=10)

    # Other fields as needed...

class ReversiGame:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()

    def initialize_board(self):
        self.board[3][3], self.board[4][4] = 'W', 'W'
        self.board[3][4], self.board[4][3] = 'B', 'B'

    # Add other methods for placing pieces, flipping, checking valid moves, etc.
