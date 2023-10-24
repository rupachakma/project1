from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signuppage,name="signuppage"),
    path('loginpage', views.loginpage,name="loginpage"),
    path('logoutpage', views.logoutpage,name="logoutpage"),
    path('adminpage', views.adminpage,name="adminpage"),
    path('myprofile', views.myprofile,name="myprofile"),
    path('profileupdate', views.profileupdate,name="profileupdate"),
    path('changepassword', views.changepassword,name="changepassword"),
    path('addstudent', views.addstudent,name="addstudent"),

]
