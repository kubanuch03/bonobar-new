from django.db import models
from apps.category.models import Category, SubCategory


class Wine(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to="wine_pictures/%Y/%m/%d/")
    gram = models.FloatField(help_text="Information about the item's weight", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='wine_category')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='wine_subcategory')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wine: {self.title}, price: {self.price}"
