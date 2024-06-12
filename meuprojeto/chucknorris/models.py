from django.db import models

class FavoriteJoke(models.Model):
    joke = models.TextField()

    def __str__(self):
        return self.joke
