from django.urls import path
from . import views

urlpatterns = [
    path('',          views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('register/', views.register_view, name='register'),
    path('home/',     views.home_view,     name='home'),
    path('upcoming/', views.upcoming_view, name='upcoming'),
    path('me/',       views.me_view,       name='me'),
    path('me/edit/',  views.me_edit_view,  name='me_edit'),
    path('history/',  views.history_view,  name='history'),
    path('book/',     views.book_view,     name='book'),
]