from django.db import models


class Game(models.Model):
    """
    Represents a game.
    """
    name = models.CharField(max_length=50, blank=False)
    slug = models.CharField(max_length=20, blank=False)
    author = models.CharField(max_length=50, blank=True)
