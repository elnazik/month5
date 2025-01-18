from rest_framework import serializers
from .models import Director, Movie, Review




class DirectorNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate(self, attrs):
        name = attrs.get('name')


class ReviewStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    stars = serializers.IntegerField()
    movie = serializers.IntegerField()

    class Meta:
        model = Review
        fields = '__all__'

class ReviewValidateSerializer(serializers.Serializer):
    stars = serializers.IntegerField()
    movie = serializers.IntegerField()

    def validate(self, attrs):
        stars = attrs.get('stars')
        movie = attrs.get('movie')


class MovieTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_average_rating(self, review):
        reviews = Review.objects.all()
        if reviews:
            sum_reviews = sum(i.stars for i in reviews)
            average = sum_reviews / len(reviews)
            return average
        return None

class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    stars = serializers.IntegerField()


    def validate(self, attrs):
        title = attrs.get('title')
        description = attrs.get('description')
        stars = attrs.get('stars')


