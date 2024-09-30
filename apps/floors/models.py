from django.db import models
from validators.validator import validate_alphanumeric



class Floor(models.Model):
    title = models.CharField(max_length=255, unique=True, validators=[validate_alphanumeric])
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.title
    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]


