from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cuisine = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username + " " + self.name



