from django.db import models
from validators.validator import validate_alphanumeric
from .validators import validate_file_size


class BanerMain(models.Model):
    title = models.CharField(max_length=255, unique=True, validators=[validate_alphanumeric])
    subtitle = models.CharField(max_length=255, unique=True)
    topik_baner = models.ManyToManyField('BanerMainTopik')

    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]

class BanerMainTopik(models.Model):
    
    img = models.ImageField(upload_to="baner_main/%Y/%m/%d/", validators=[validate_file_size])
    created_at = models.DateTimeField(auto_now_add=True)

class BanerMiddle(models.Model):
    title = models.CharField(max_length=255, unique=True, validators=[validate_alphanumeric])
    img = models.FileField(upload_to='baner_middle/%Y/%m/%d',)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]
    
class BanerBook(models.Model):
    title = models.CharField(max_length=255, unique=True, validators=[validate_alphanumeric])
    img = models.ImageField(upload_to="baner_book/%Y/%m/%d/", validators=[validate_file_size])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]