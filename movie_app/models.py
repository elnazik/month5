from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    duration = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

STARS = (
    (1, '*'),
    (2, '* *'),
    (3, '* * *'),
    (4, '* * * *'),
    (5, '* * * * *'),
)

class Review(models.Model):
    stars = models.IntegerField(choices=STARS, default=1)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField(blank=True)
    def __str__(self):
        return self.text