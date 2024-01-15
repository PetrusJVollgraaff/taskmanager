from django import forms
from .models import *



def CheckCookie(request):
    displayby = request.COOKIES.get('project_by')
    
    return displayby if displayby in ["priority", "type"] else "date"

def UpdateLog(project, task, staff, note):
    
    
    if task is None :
        logC = Log(project = project, staff=staff, lognote=note)
    else:
        logC = Log(project = project, task=task, staff=staff, lognote=note)
    
    logC.save()