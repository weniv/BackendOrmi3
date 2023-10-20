from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=50)

    def __str__(self):
        return self.title