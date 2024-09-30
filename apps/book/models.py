from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255,blank=True,null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    will_come = models.DateField(blank=True,null=True)
    time_stamp_h = models.TimeField(blank=True,null=True)   #время провождение
    time_stamp = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    amount_guest = models.PositiveIntegerField()
    comment = models.TextField(blank=True,null=True)
    is_come = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user_name}"

    def get_tables(self):
        return ", ".join(str(table.number_table) for table in self.tables.all())

    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]
