from django.db import models
from django.core.validators import MinValueValidator


from apps.category.models import Category, SubCategory


class Menu(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField(blank=True, null=True,validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to="menu_pictures/%Y/%m/%d/")
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='menu_parent')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, related_name='menu_subcategory', default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Menu: {self.title}, price: {self.price}"
