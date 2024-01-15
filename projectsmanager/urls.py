from django.urls import path

from . import views, login, createproject, actionproject

urlpatterns = [
    path('', views.index, name='index'),
    path("login", login.login_view, name="login"),
    path("logout", login.logout_view, name="logout"),
    path("register", login.register, name="register"),
    path("create", createproject.create, name="create"),
    path("edit", createproject.edit, name="edit"),
    path("delete", createproject.delete, name="delete"),
    path("myprojects", createproject.myprojects, name="myprojects"),
    path('fectstaffs', createproject.fectstaffs, name='fectstaffs'),
    path('projectCreate', createproject.projectCreate, name='projectCreate'),
    path('projectEdit', createproject.projectEdit, name='projectEdit'),
    path('getEditDetails', createproject.getEditDetails, name='getEditDetails'),
    path('projectDetail', actionproject.projectDetail, name='projectDetail'),
    path('getDetails', actionproject.getDetails, name='getDetails'),
    path('taskstatus', actionproject.taskstatus, name='taskstatus'),
    path('projectstatus', actionproject.projectstatus, name='projectstatus')
]
