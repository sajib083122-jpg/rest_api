from django.db import models

# Create your models here.

class Book(models.Model):
    book_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)  # Add a slug field to the model


    # def __str__(self):                 # string Re-presentation at admin pannle
    #     return self.book_name