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

    # Student Path..
    path('addstudent', views.addstudent,name="addstudent"),
    path('studentlist', views.studentlist,name="studentlist"),
    path('editstudent<str:id>',views.editstudent,name="editstudent"),
    path('deletestudent<str:id>',views.deletestudent,name="deletestudent"),
    path('updatestudent',views.updatestudent,name="updatestudent"),

    # Teacher Path
    path('addteacher', views.addteacher,name="addteacher"), 
    path('teacherlist', views.teacherlist,name="teacherlist"), 
    path('editteacher', views.editteacher,name="editteacher"), 
    path('teacherdelete<str:id>', views.teacherdelete,name="teacherdelete"), 

    # Department Path
    path('adddepartment', views.adddepartment,name="adddepartment"), 
    path('departmentlist', views.departmentlist,name="departmentlist"), 
    path('editdepartment<str:id>', views.editdepartment,name="editdepartment"), 
    path('updatedepartment', views.updatedepartment,name="updatedepartment"), 
    path('departmentdelete<str:id>', views.departmentdelete,name="departmentdelete"), 

    # Subject Path
    path('addsubject', views.addsubject,name="addsubject"), 
    path('subjectlist', views.subjectlist,name="subjectlist"), 
    path('editsubject<str:id>', views.editsubject,name="editsubject"), 
    path('updatesubject', views.updatesubject,name="updatesubject"),
]

