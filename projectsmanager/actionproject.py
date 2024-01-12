import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.db.models.functions import Now
from .SQL import *
from .functions import *
import json
from urllib import parse

@csrf_exempt
@login_required(login_url='/')
def projectDetail(request):    
    return render(request, "projects/project.html")

@csrf_exempt
@login_required(login_url='/')
def getDetails(request):
    referer_url = request.META.get('HTTP_REFERER')
    parsed      = parse.urlparse(referer_url)
    pid         = re.sub(r"pid\=([\d]+)", r"\1", parsed.query)

    return JsonResponse(ProjectDetails(pid)[0], safe=False )

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
            TaskAssignTo.objects.filter(
                Q(tasks_id = taskid, project_id=projectid, staffassign_id=loginUserid.id) |
                Q(tasks_id = taskid, project_id=projectid, staffadd_id=loginUserid.id)
            ).update( status=taskstatus )
            
            UpdateLog(project, task, loginUserid, f"Task status change to {taskstatus}" )
            status['status'] = 'success'
            status['message'] = 'Task successfully saved'
        except Exception as e:    
            print(e)
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
            Projects.objects.filter(project_id=projectid, staffadd_id=loginUserid.id).update( status=projectstatus, completeddate=Now() )
            UpdateLog(project, None, loginUserid, f"Project status change to {projectstatus}" )
            
            status['status'] = 'success'
            status['message'] = 'Task successfully saved'
        except Exception as e:    
            status['status'] = 'error'
            status['message'] = 'An Error has occured'
    
    return JsonResponse(status, safe=False )
