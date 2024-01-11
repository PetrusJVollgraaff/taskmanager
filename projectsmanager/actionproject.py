from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .SQL import *
from .functions import *
import json

@csrf_exempt
@login_required(login_url='/')
def taskstatus(request):
    status = {}
    if request.method == 'POST':
        jsonData    = json.loads(request.body)
        taskid      = int( jsonData.get("taskid") )
        projectid   = int( jsonData.get("projectid") )
        taskstatus  = jsonData.get("status")

        loginUserid  = User.objects.get(id=request.user.id)
        project     = Projects.objects.get(id=projectid)
        task        = Tasks.objects.get(id=taskid)
        
        try:    
            TaskAssignTo.objects.filter(tasks_id = taskid, project_id=projectid, staff_id=loginUserid).update( status=taskstatus )
            
            UpdateLog(project, task, loginUserid, "Task status change to {taskstatus}" )
            status['status'] = 'success'
            status['message'] = 'Task successfully saved'
        except Exception as e:    
            status['status'] = 'error'
            status['message'] = 'An Error has occured'
        
    return JsonResponse(status, safe=False )

@csrf_exempt
@login_required(login_url='/')
def projectstatus(request):
    status = {}
    if request.method == 'POST':
        jsonData        = json.loads(request.body)
        projectid       = int( jsonData.get("projectid") )
        projectstatus   = jsonData.get("status")

        loginUserid     = User.objects.get(id=request.user.id)
        project         = Projects.objects.get(id=projectid)
        
        try:    
            Projects.objects.filter(project_id=projectid, staffadd_id=loginUserid).update( status=projectstatus )
            
            UpdateLog(project, None, loginUserid, "Project status change to {projectstatus}" )
            status['status'] = 'success'
            status['message'] = 'Task successfully saved'
        except Exception as e:    
            status['status'] = 'error'
            status['message'] = 'An Error has occured'
    
    return JsonResponse(status, safe=False )
