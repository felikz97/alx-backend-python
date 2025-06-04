from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.
class user(AbstractUser):
    user_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    first_name = models.CharField(max_length=25,null=False)
    last_name = models.CharField(max_length=25,null=False)
    password = models.CharField(min_length=8,null=False)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.email
    
class message(models.Model):
    pass
class conversation(models.Model):
    pass