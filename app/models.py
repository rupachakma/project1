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
    profilepic = models.ImageField(upload_to="media/profileimg", blank=True, null=True)

class Coursemodel(models.Model):
    name = models.CharField(max_length=50)
    createat = models.DateTimeField(auto_now_add=True)
    updateat = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Sessionyearmodel(models.Model):
    sessionstart = models.CharField(max_length=50)
    sessionend = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.sessionstart +'-'+ self.sessionend
    
class Studentmodel(models.Model):
    admin = models.OneToOneField(customUser, on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=50)
    courseid = models.ForeignKey(Coursemodel,on_delete=models.DO_NOTHING,default=1)
    sessionid = models.ForeignKey(Sessionyearmodel,on_delete=models.DO_NOTHING,default=1)
    createat = models.DateTimeField(auto_now_add=True)
    updateat = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.admin.first_name +'-'+self.admin.last_name