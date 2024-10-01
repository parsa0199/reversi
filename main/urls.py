from django.urls import path
from .views import (
    HomeView,
    AboutView,
    ContactView,
    PrivicyView,
    Privicy2View,
    EduView,
    DiseView,
)

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('درباره-ما/', AboutView.as_view(), name='about'),
    path('edu/', EduView.as_view(), name='edu'),
    path('privacy/', PrivicyView.as_view(), name='privacy'),
    path('تماس-با-ما/', ContactView.as_view(), name='contact'),
    path('سیاست-حفظ-حریم-خصوصی-2/', Privicy2View.as_view(), name='privacy2'),
    path('dise/', DiseView.as_view(), name='dise'),
]
