from django.urls import path

from . import views, login, createproject, actionproject

urlpatterns = [
    path('', views.index, name='index'),
    path("login", login.login_view, name="login"),
    path("logout", login.logout_view, name="logout"),
    path("register", login.register, name="register"),
    path("create", createproject.create, name="create"),
    path('fectstaffs', createproject.fectstaffs, name='fectstaffs'),
    path('projectCreate', createproject.projectCreate, name='projectCreate'),
    path('projectDetail', actionproject.projectDetail, name='projectDetail'),
    path('taskstatus', actionproject.taskstatus, name='taskstatus'),
    path('projectstatus', actionproject.projectstatus, name='projectstatus'),
    #path("myprojects", projects.myprojects, name="myprojects"),
]
