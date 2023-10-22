from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from app.models import customUser

# Create your views here.
def home(request):
    return render(request,"base.html")

def signuppage(request):
    error_message = {
        'password_error' : 'Password not match'
    }
    if request.method == "POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        pass1=request.POST.get("password")
        pass2=request.POST.get("confirmpassword")
        if pass1 == pass2:
            myuser = customUser.objects.create_user(name,email,pass1)
            myuser.save()
            return redirect("loginpage")
        else:
            messages.error(request,error_message['password_error'])

    return render(request,"signup.html")

def loginpage(request):
    error_messages = {
        'login_error':'Invalid Username or Password'
    }
    if request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username = name,password = password)
        if user is not None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return redirect("adminpage") 
            elif user_type == '2':
                return redirect("staffpage")
            elif user_type == '3':
                return redirect("studentpage")
            else:
                return redirect("signuppage")
        else:
            messages.error(request,error_messages['login_error'])
    return render(request,"login.html")

def adminpage(request):
    return render(request,"myadmin/adminhome.html")

def myprofile(request):
    user = request.user
    data = {
        'user':user
    }
    return render(request,"profile.html",data)

def profileupdate(request):
    error_messages = {
        'success':'Profile update successfully',
        'error':'Profile not Updated '
    }
    if request.method == "POST":
        username = request.POST.get("username"),
        first_name = request.POST.get("first_name"),
        last_name = request.POST.get("last_name"),
        password = request.POST.get("password"),
        email = request.POST.get("email"),
        profilepic = request.FILES.get("profile_pic"),