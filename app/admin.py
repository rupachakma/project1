from django.contrib import admin
from django.contrib.auth.admin import  UserAdmin
from app.models import Coursemodel, Sessionyearmodel, Studentmodel, customUser

# Register your models here.
class userModel(UserAdmin):
    list_display=['id','username','user_type']

admin.site.register(customUser,userModel)
admin.site.register(Coursemodel)
admin.site.register(Sessionyearmodel)
admin.site.register(Studentmodel)