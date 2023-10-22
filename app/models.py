from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#customUser
class customUser(AbstractUser):
    USER = (
        (1,"admin"),
        (2,"staff"),
        (3,"student"),
    )
    user_type = models.CharField(choices=USER,max_length=50,default=1)
    profileimg = models.ImageField(upload_to="media/profileimg", blank=True, null=True)