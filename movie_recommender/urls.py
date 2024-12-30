from django.contrib import admin
from django.urls import path
from movie_recommender import views
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("search_movie/", views.search_movies, name="search_page"),
    path('clear-session/', views.clear_session, name='clear_session'),
    path('movie/<str:movie_id>/', views.movie_detail, name='movie_detail'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # path('login/', views.login_view, name='login'),
    # path('signup/', views.signup_view, name='signup'),
    # path('register/', views.register, name='register'),
]