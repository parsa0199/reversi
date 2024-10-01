from django.urls import path
from . views import *

app_name = 'dashboard'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('messages/', MessagesView.as_view(), name='messages'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),

]
