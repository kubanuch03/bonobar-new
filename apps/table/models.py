from django.db import models
from apps.floors.models import Floor
from apps.book.models import Book


class Table(models.Model):
    number_table = models.PositiveIntegerField()
    books = models.ManyToManyField(Book, related_name='tables', blank=True)
    occupated = models.BooleanField(default=False)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.number_table}"

    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]
