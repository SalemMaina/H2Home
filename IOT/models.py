from django.db import models

class RandomNumber(models.Model):
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.value} at {self.created_at}"