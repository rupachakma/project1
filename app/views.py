from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from app.models import Coursemodel, Sessionyearmodel, Studentmodel, Teachermodel,Subjectmodel, customUser
from django.contrib.auth import login as auth_login

# Create your views here.
def home(request):
    return render(request,"base.html")

def signuppage(request):
    error_message = {
        'password_error':'Password not match',
        'username_error':'User name already exist',
        'email_error':'Email alredy exist'
    }
    if request.method == "POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        pass1=request.POST.get("password")
        pass2=request.POST.get("confirmpassword")
        if pass1 == pass2:
            if customUser.objects.filter(email=email).exists():
                messages.error(request,error_message['email_error'])
            elif customUser.objects.filter(username=name).exists():
                messages.error(request,error_message["username_error"])
            else:
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
    teacher = Teachermodel.objects.all().count
    student =Studentmodel.objects.all().count
    subject = Subjectmodel.objects.all().count
    context = {
        'teacher':teacher,
        'student':student,
        'subject':subject,

    }
    return render(request,"myadmin/adminhome.html",context)

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

def addstudent(request):
    error_messages = {
        'success':'Student add Successfully',
        'error':'Already exists'
    }
    if request.method == "POST":
       firstname = request.POST.get("first_name")
       lastname = request.POST.get("last_name")
       email = request.POST.get("email")
       username = request.POST.get("username")
       password = request.POST.get("password")
       address = request.POST.get("address")
       gender = request.POST.get("gender")
       courseid = request.POST.get("courseid")
       sessionid = request.POST.get("sessionyearid")
       profilepic = request.FILES.get("profilepic")

       if customUser.objects.filter(email=email).exists() or customUser.objects.filter(password=password).exists():
           messages.error(request,error_messages["error"])
       else:
           user = customUser.objects.create_user(username,password,email)
           user.first_name = firstname
           user.last_name = lastname
           user.profilepic = profilepic
           user.user_type = 3
           user.save()

           usercourse = Coursemodel.objects.get(id=courseid)
           sessionyear = Sessionyearmodel.objects.get(id=sessionid)
           
           student = Studentmodel(
               admin = user,
               address = address,
               sessionid = sessionyear,
               courseid = usercourse,
               gender = gender
           )
           student.save()
           messages.success(request,error_messages["success"])
           return redirect("addstudent")

    course = Coursemodel.objects.all()
    session = Sessionyearmodel.objects.all()
    context = {
        'course':course,
        'session':session,
    }
    return render(request,'student/addstudent.html',context)

def studentlist(request):
    allstudent = Studentmodel.objects.all()
    return render(request,"student/studentlist.html",{'allstudent':allstudent})

def editstudent(request,id):
    studentid = Studentmodel.objects.filter(id=id)
    course = Coursemodel.objects.all()
    session = Sessionyearmodel.objects.all()

    context = {
        'student':studentid,
        'course':course,
        'session':session,
    }

    return render(request,"student/editstudent.html",context)

def updatestudent(request):
    error_messages = {
        'success':'Student update Successfully',
        'error':'Student update failed'
    }
    if request.method == "POST":
       studentid = request.POST.get("student_id")
       firstname = request.POST.get("first_name")
       lastname = request.POST.get("last_name")
       email = request.POST.get("email")
       username = request.POST.get("username")
       password = request.POST.get("password")
       address = request.POST.get("address")
       gender = request.POST.get("gender")
       courseid = request.POST.get("courseid")
       sessionid = request.POST.get("sessionyearid")
       profilepic = request.FILES.get("profilepic")

       user = customUser.objects.get(id=studentid)
       user.first_name = firstname
       user.last_name = lastname
       user.email = email
       user.username = username

       if password is not None:
          user.set_password(password)
       if profilepic is not None:
          user.profilepic = profilepic
       user.save()

       student = Studentmodel.objects.get(admin = studentid)
       student.address = address,
       student.gender = gender,

       session = Sessionyearmodel.objects.get(id=sessionid)
       student.sessionid=session

       course=Coursemodel.objects.get(id=courseid)
       student.courseid=course
       student.save()
       messages.success(request,error_messages["success"])
       return redirect("studentlist")

    return render(request,"student/editstudent.html")

def deletestudent(request,id):
    student = Studentmodel.objects.get(id=id)
    student.delete()
    return redirect("studentlist")

def addteacher(request):
    error_messages = {
        'success':'Teacher add successfully',
        'error':'Already exists'
    }
    if request.method == "POST":
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        courseid = request.POST.get("courseid")
        mobile = request.POST.get("mobile")
        experience = request.POST.get("experience")
        profilepic = request.FILES["profilepic"]

        if customUser.objects.filter(email=email).exists():
            messages.error(request,error_messages["error"])
        elif customUser.objects.filter(username=username).exists():
            messages.error(request,error_messages["error"])
        else:
            user = customUser.objects.create_user(username=username,email=email,password=password)
            user.first_name = firstname
            user.last_name = lastname
            user.profilepic = profilepic
            user.user_type = 2
            user.save()
            courseid = Coursemodel.objects.get(id=courseid)

            teacher = Teachermodel(
                admin = user,
                address = address,
                gender = gender,
                mobile = mobile,
                courseid = courseid,
                experience = experience
            )
            teacher.save()
            messages.success(request,error_messages["success"])
            return redirect("addteacher")
    course = Coursemodel.objects.all()
    context = {
        'course':course
    }

    return render(request,"teacher/addteacher.html",context)

def teacherlist(request):
    teacher = Teachermodel.objects.all()
    return render(request,"teacher/teacherlist.html",{'teacher':teacher})

def editteacher(request,id):
    teacher = Teachermodel.objects.filter(id=id)
    course = Coursemodel.objects.all()
    context = {
        'teacher':teacher,
        'course':course,
    }

    return render(request,"teacher/editteacher.html",context)

def updateteacher(request):
    error_messages = {
        'success':'Teacher Update successfully',
        'error':'Teacher update failed'
    }
    if request.method == "POST":
        teacherid = request.POST.get("teacher_id")
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        courseid = request.POST.get("courseid")
        mobile = request.POST.get("mobile")
        experience = request.POST.get("experience")
        profilepic = request.FILES["profilepic"]

        user = customUser.objects.get(id=teacherid)
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.username = username

        if password is not None:
            user.set_password(password)
        if profilepic is not None:
            user.profilepic = profilepic
        user.save()

        teacher = Teachermodel.objects.get(admin = teacherid)
        teacher.address = address,
        teacher.gender = gender,
        teacher.mobile = mobile,
        teacher.experience = experience

        course=Coursemodel.objects.get(id=courseid)
        teacher.courseid=course
        teacher.save()
        messages.success(request,error_messages["success"])
        return redirect("teacherlist")
    
    return render(request,"teacher/editteacher.html")

def teacherdelete(request,id):
    teacher = Teachermodel.objects.get(id=id)
    teacher.delete()
    return redirect("teacherlist")   

def adddepartment(request):
    error_messages = {
        'success':'Department add successfully',
        'error':'Already exists'
    }
    if request.method == "POST":
        dept_name = request.POST.get("department_name")

        if Coursemodel.objects.filter(name=dept_name):
            messages.error(request,error_messages['error'])
        else:
            course = Coursemodel(
                name = dept_name,
            )
            course.save()
            messages.success(request,error_messages["success"])
            return redirect("adddepartment")

    return render(request,"department/adddepartment.html")

def departmentlist(request):
    department = Coursemodel.objects.all()
    return render(request,"department/departmentlist.html",{'department':department})

def editdepartment(request,id):
    
    course = Coursemodel.objects.get(id=id)
    context = {
        "course": course,
    }
    
    return render(request,"department/editdepartment.html",context)

def updatedepartment(request ):
    error_messages = {
        'success': 'Department Updated Successfully',
        'error': 'Department Update Failed',
    }
    if request.method == "POST":
        department_id = request.POST.get("department_id")
        department_name = request.POST.get("department_name")

        course = Coursemodel.objects.get(id=department_id)
        course.name = department_name
        course.save()
        messages.success(request,error_messages["success"])
        return redirect("departmentlist")
    else:
        messages.error(request,error_messages["error"])
    return render(request,"department/editdepartment.html")
  
def departmentdelete(request,id):
    dept = Coursemodel.objects.get(id=id)
    dept.delete()
    return redirect("departmentlist")

def addsubject(request):
    error_messages = {
        'success':'Subject add successfully',
        'error':'Already exists'
    }
    if request.method == "POST":
        sub_id = request.POST.get("subject_id")
        sub_name = request.POST.get("subject_name")
        courseid = request.POST.get("course_id")
        teacherid = request.POST.get("teacher_id")
        
        courseid = Coursemodel.objects.get(id=courseid)
        teacherid = Teachermodel.objects.get(id=teacherid)

        sub = Subjectmodel(
        name = sub_name,
        course = courseid,
        teacher = teacherid
        )
        sub.save()
        messages.success(request,error_messages["success"])
        return redirect("addsubject")
    
    course = Coursemodel.objects.all()
    teacher = Teachermodel.objects.all()
    context = {
        'course':course,
        'teacher':teacher
    }
    return render(request,"subjects/addsubject.html",context)

def subjectlist(request):
    subject = Subjectmodel.objects.all()
    return render(request,"subjects/subjectlist.html",{'subject':subject})

def editsubject(request,id):
    subject = Subjectmodel.objects.filter(id=id)
    course=Coursemodel.objects.all()
    teacher=Teachermodel.objects.all()
    context = {
        'subject':subject,
        'course':course,
        'teacher':teacher
    }
    return render(request,"subjects/editsubject.html",context)

def updatesubject(request):
    error_messages = {
        'success': 'Subject Updated Successfully',
        'error': 'Subject Update Failed',
    }
    if request.method == "POST":
        sub_id = request.POST.get("subject_id")
        sub_name = request.POST.get("subject_name")
        course = request.POST.get("course_id")
        teacher = request.POST.get("teacher_id")
        
        subject = Subjectmodel.objects.get(id=sub_id)
        subject.name = sub_name
        course = Coursemodel.objects.get(id=course)
        subject.course = course
        teacher = Teachermodel.objects.get(id=teacher)
        subject.teacher = teacher

        subject.save()
        messages.success(request, error_messages['success'])
        return redirect("subjectlist")
    
    return render(request,"subjects/editsubject.html")


def subjectdelete(request,id):
    subject = Subjectmodel.objects.get(id=id)
    subject.delete()
    return redirect("subjectlist")
