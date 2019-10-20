from django.db import models
from django.contrib.auth.models import User

class add_userinfo(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    long = models.FloatField()
    lat = models.FloatField()
    local_address = models.CharField(max_length = 100)
    phone = models.IntegerField()
    
