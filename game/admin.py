from django.contrib import admin

# Register your models here.
from game.models import Game,ReversiGame

admin.site.register(Game)

# admin.site.register(ReversiGame)