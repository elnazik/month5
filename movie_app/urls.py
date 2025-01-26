from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/director/', views.DirectorListCreateAPIView.as_view()),
    path('<int:id>/', views.director_detail_api_view),
    path('api/v1/movie/', views.movie_list_api_view),
    path('<int:id>/', views.movie_detail_api_view),
    path('api/v1/review/', views.review_list_api_view),
    path('<int:id>/', views.review_detail_api_view),
    path('reviews', views.ReviewListAPIView.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetailAPIView.as_view()),
    path('movies', views.MovieViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('movies/<int:pk>/', views.MovieViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    })),
]
