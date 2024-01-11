from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .SQL import *
from .functions import *
import json

def create(request):

    priorities  = getPriorities()
    types       = getTypes()

    return render(request, "projects/create.html",{"priorities": priorities, "types": types})

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
        print(jsonData)
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
        
        print( tasks )
        
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