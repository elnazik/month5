from collections import OrderedDict
from wsgiref.validate import validator

from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (DirectorSerializer,
                          MovieSerializer,
                          ReviewSerializer,
                          DirectorNameSerializer,
                          MovieTitleSerializer,
                          ReviewStarSerializer,
                          MovieValidateSerializer,
                          DirectorValidateSerializer,
                          ReviewValidateSerializer)
from .models import Director, Movie, Review
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

class DirectorListCreateAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def create(self, request, *args, **kwargs):
        validator = DirectorValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': validator.errors})
        name = validator.validated_data['name']

        with transaction.atomic():
            product = Director.objects.create(
                name=request.data['name'],
                director=request.data['director'],
            )
            director = Director.objects.create()
            director.director_id = director.id

        return Response(status=status.HTTP_201_CREATED,
                        data=DirectorSerializer(product).data)


class CustomPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer()
    pagination_class = CustomPagination

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer()
    pagination_class = CustomPagination

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer()
    lookup_field = 'id'

@api_view(http_method_names=['GET', 'POST'])
def director_list_create_api_view(request):
    print(request.user)
    if request.method == 'GET':
        directors = Director.objects.all()

        list_ = DirectorSerializer(instance=directors, many=True).data

        return Response(data=list_)
    elif request.method == 'POST':
        validator= DirectorValidateSerializer(data=request.data)
        if validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=validator.errors)

        name = request.data.get('name')
        with transaction.atomic():
            director = Director.objects.create(name=name)

        director.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=DirectorSerializer(director).data)



@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all(id=id)
        data = DirectorSerializer(instance=directors).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.data.get('name'):
            Director.directors = request.data.get('directors')
        Director.save()
        return Response(data=DirectorNameSerializer(Director).data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        Director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(http_method_names=['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()

        list_ = MovieSerializer(instance=movies, many=True).data
        return Response(data=list_)
    elif request.method == 'POST':
        validator= MovieValidateSerializer(data=request.data)
        if validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=validator.errors)

        title = request.data.get('title')
        description = request.data.get('description')
        director = request.data.get('director')
        duration = request.data.get('duration')
    with transaction.atomic():
        Movie.objects.create(title=title,
                         description=description,
                         director=director,
                         duration=duration)
    Movie.save()

    return Response(status=status.HTTP_201_CREATED,
                    data=MovieSerializer(Movie).data)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all(id=id)
        data = MovieSerializer(instance=movies).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Movie.title = request.data.get('title')
        Movie.description = request.data.get('description')
        Movie.director = request.data.get('director')
        Movie.duration = request.data.get('duration')
        Movie.save()
        return Response(data=MovieTitleSerializer(Movie).data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        Movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(http_method_names=['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        list_ = ReviewSerializer(instance=reviews, many=True).data
        return Response(data=list_)
    elif request.method == 'POST':
        validator = ReviewValidateSerializer(data=request.data)
        if validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=validator.errors)
        stars = request.data.get('stars')
        movie_id = request.data.get('movie_id')
        with transaction.atomic():
            Review.objects.create(stars=stars, movie_id=movie_id)
        Review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data= ReviewStarSerializer(Review).data)
@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all(id=id)
        data = ReviewSerializer(instance=reviews).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Review.stars = request.data.get('stars')
        Review.movie_id = request.data.get('movie_id')
        Review.save(data=ReviewStarSerializer(Review).data,
                    status=status.HTTP_201_CREATED)
        return Response()
    elif request.method == 'DELETE':
        Review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

