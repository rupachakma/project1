from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from app.models import customUser
from django.contrib.auth import login as auth_login

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

def logoutpage(request):
    logout(request)
    return redirect("loginpage")

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
        'success': 'Profile Update Successfully',
        'error': 'Profile Not Updated',
        'password_error': 'Current password is incorrect',
    }
    
    if request.method == "POST":
        profilepic = request.FILES.get('profilepic')
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        password = request.POST.get("password")
        username = request.POST.get("username")
        email = request.POST.get("email")
    
        cuser = customUser.objects.get(id=request.user.id)
        cuser.first_name = firstname
        cuser.last_name = lastname
        cuser.profilepic = profilepic
        
        # Verify the current password provided matches the user's current password
        if not cuser.check_password(password):
            messages.error(request, error_messages['password_error'])
        else:
            # If the current password is correct, proceed to update other fields
            if profilepic is not None:
                cuser.profilepic = profilepic
            
            # You can add additional fields to update here as needed
            cuser.save()
            auth_login(request, cuser)
            messages.success(request, error_messages['success'])
            return redirect("profileupdate")

    return render(request, 'profile.html')

def changepassword(request):
    error_messages = {
        'success':'Changed successfully',
        'mismatched_error':'New password and old password not matched',
        'oldpassword':'Old password not match',
    }
    if request.method == "POST":
        oldpassword = request.POST.get("oldPassword")
        newpassword = request.POST.get("newpassword")
        confirmPassword = request.POST.get("confirmPassword")
        user = request.user
        if user.check_password(oldpassword):
            if newpassword == confirmPassword:
                user.set_password(newpassword)
                user.save()
                messages.success(request,error_messages["success"])
                return redirect("loginpage")
            else:
                messages.error(request,error_messages["mismatched_error"])
        else:
            messages.error(request,error_messages["oldpassword"])
        
    return render(request,"changepassword.html")