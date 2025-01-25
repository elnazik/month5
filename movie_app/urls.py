from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/director/', views.director_list_api_view),
    path('api/v1/directors/<int:id>/', views.director_detail_api_view),
    path('api/v1/movie/', views.movie_list_api_view),
    path('api/v1/movies/<int:id>/', views.movie_detail_api_view),
    path('api/v1/review/', views.review_list_api_view),
    path('api/v1/reviews/<int:id>/', views.review_detail_api_view),
]
