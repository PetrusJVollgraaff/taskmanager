import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models.functions import Now
from django.shortcuts import render
from .SQL import *
from .functions import *
from urllib import parse
import json


@csrf_exempt
@login_required(login_url='/')
def create(request):

    priorities  = getPriorities()
    types       = getTypes()

    return render(request, "projects/create.html",{"priorities": priorities, "types": types})


@csrf_exempt
@login_required(login_url='/')
def edit(request):
    priorities  = getPriorities()
    types       = getTypes()

    return render(request, "projects/edit.html",{"priorities": priorities, "types": types})

@csrf_exempt
@login_required(login_url='/')
def getEditDetails(request):
    referer_url = request.META.get('HTTP_REFERER')
    parsed      = parse.urlparse(referer_url)
    pid         = re.sub(r"pid\=([\d]+)", r"\1", parsed.query)

    return JsonResponse(ProjectEditDetails(pid)[0], safe=False )

@csrf_exempt
@login_required(login_url='/')
def myprojects(request):
    user            = request.user
    projectz        = MyProject(user.id)
    displayby       = CheckCookie(request)
    displaytitle    = {"priority": "Priority", "type": "Type"}.get(displayby, "Create Date")
    orderbyz        = {"priority": "level", "type": "typename"}.get(displayby, "addeddate")

    projectz.sort(key = lambda x:x[orderbyz])
    return render(request, "projects/main.html",{"projects": projectz, "displayby": displaytitle, "delete": 1})


@csrf_exempt
@login_required(login_url='/')
def delete(request):
    status = {}

    if request.method == 'POST':
        jsonData    = json.loads(request.body)
        projectid   = int( jsonData.get("pid") )
        userdetail  = User.objects.get(id=request.user.id)

        try:
            Projects.objects.filter(id = projectid, staffadd_id = userdetail.id).update( isDeleted = True, staffdelete_id = userdetail, removedate = Now())
            
            status['status'] = 'success'
            status['message'] = 'Project is successfully Deleted'
        except Exception as e:  
            status['status'] = 'error'
            status['message'] = 'Could not delete this Project'
        
    return JsonResponse(status, safe=False )


@csrf_exempt
@login_required(login_url='/')
def fectstaffs(request):
    return JsonResponse(getStaff(), safe=False )


@csrf_exempt
@login_required(login_url='/')
def projectCreate(request):
    status = {}

    if request.method == 'POST':
        jsonData    = json.loads(request.body)
        title       = jsonData.get("name")
        descript    = jsonData.get("descript")
        typeid      = int( jsonData.get("type") )
        priorityid  = int( jsonData.get("priority") )
        duedate     = jsonData.get("duedate")
        tasks       = jsonData.get("tasks")
        
        userdetail  = User.objects.get(id=request.user.id)
        priority    = Priority.objects.get(id=priorityid)
        type        = Type.objects.get(id=typeid)
        
        projectC = Projects(name=title, descript=descript, status="open", priority=priority, type=type, staffadd=userdetail)
        projectC.save()
        UpdateLog(projectC, None, userdetail, "Project Created")

        
        for i,task in enumerate(tasks):
            staff           = User.objects.get(id=task.get("staffid"))
            taskname        = task.get("name")
            taskdescript    = task.get("descript")

            taskC = Tasks(name=taskname, descript=taskdescript, staffadd=staff)
            taskC.save()

            protask    = ProjectsTasks(tasks=taskC, project=projectC)
            protask.save()

            assignto    = TaskAssignTo(tasks=taskC,  project=projectC, staffassign=staff, staffadd=userdetail, status="open",)
            assignto.save()

            UpdateLog(projectC, taskC, userdetail, "Project Task Created")

        status['status'] = 'success'
        status['message'] = 'Project is successfully Added'
        
    return JsonResponse(status, safe=False )


@csrf_exempt
@login_required(login_url='/')
def projectEdit(request):
    status = {}

    if request.method == 'POST':
        jsonData    = json.loads(request.body)
        mainprojectid =  int( jsonData.get("id") )
        title       = jsonData.get("name")
        descript    = jsonData.get("descript")
        typeid      = int( jsonData.get("type") )
        priorityid  = int( jsonData.get("priority") )
        duedate     = jsonData.get("duedate")
        tasks       = jsonData.get("tasks")
        tasksremove = jsonData.get("tasksremoved")

        userdetail  = User.objects.get(id=request.user.id)
        priority    = Priority.objects.get(id=priorityid)
        type        = Type.objects.get(id=typeid)
        MainProject = Projects.objects.get(id=mainprojectid)
        
        
        if not Projects.objects.filter(name=title, descript=descript, priority=priority, type=type ).exists():
            projectC = Projects(name=title, descript=descript, status="open", priority=priority, type=type, staffadd=userdetail)
            projectC.save()

            proPros    = ProjectProjects(mainproject = MainProject, subproject=projectC)
            proPros.save()

        '''
        for i,task in enumerate(tasks):
            staff           = User.objects.get(id=task.get("staffid"))
            taskname        = task.get("name")
            taskdescript    = task.get("descript")
            typeid          = int( task.get("id") )

            if not Tasks.objects.filter(name=taskname, descript=taskdescript, staffadd=staff ).exists():
                taskC = Tasks(name=taskname, descript=taskdescript, staffadd=staff)
                taskC.save()

                protask    = ProjectsTasks(tasks=taskC, project=projectC)
                protask.save()

                assignto    = TaskAssignTo(tasks=taskC,  project=projectC, staffassign=staff, staffadd=userdetail, status="open",)
                assignto.save()

            UpdateLog(projectC, taskC, userdetail, "Project Task Created")

        for i,task in enumerate(tasksremove):
            taskid      = task.get("id")
            task        = Tasks.objects.get(id=taskid)
            
            ProjectsTasks.objects.filter((tasks_id=task.id, project_id=MainProject.id).update(isDelete = True)

            UpdateLog(MainProject, task, userdetail, "Project Task Removed")
        '''

        UpdateLog(MainProject, None, userdetail, "Project Edited")

        status['status'] = 'success'
        status['message'] = 'Project is successfully Added'
    
        
    return JsonResponse(status, safe=False )