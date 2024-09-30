from django.db import models
from validators.validator import validate_alphanumeric


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[validate_alphanumeric])
    image = models.ImageField(upload_to="category_pictures/%Y/%m/%d/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Name: {self.name}"

    class Meta:
        verbose_name_plural = 'Categories'


class SubCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[validate_alphanumeric])
    order = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', )

    def __str__(self):
        return f"Name: {self.name}"

    class Meta:
        verbose_name_plural = 'Subcategories'
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.pk: 
            SubCategory.objects.filter(order__gte=1).update(order=models.F('order') + 1)
            self.order = 1
        else:
            old_order = SubCategory.objects.get(pk=self.pk).order
            if self.order != old_order:
                if self.order < old_order:
                    SubCategory.objects.filter(order__gte=self.order, order__lt=old_order).update(order=models.F('order') + 1)
                else:
                    SubCategory.objects.filter(order__gt=old_order, order__lte=self.order).update(order=models.F('order') - 1)
        super(SubCategory, self).save(*args, **kwargs)