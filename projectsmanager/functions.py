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

'''    
def CheckCreateProject(op):
    check = False
    priorities  = Priority.objects.filter(isDeleted=False)
    types       = Type.objects.filter(isDeleted=False)
    tasks       = Tasks.objects.filter(isDeleted=False)
    
    if op == "all":
        if priorities.count() > 0 and types.count() > 0 and tasks.count() > 0:
            check = True
    elif op == "type":
        if types.count() > 0:
            check = True
            
    return check
    
    
class PriorityForm(forms.Form):
    name        = forms.CharField(label='Priority Name', max_length=100, required=True)
    level       = forms.IntegerField(label='Priority Level',required=True, min_value=0, initial=0)
    
class TypeForm(forms.Form):
    name        = forms.CharField(label='Type Name', max_length=100, required=True)
    descript    = forms.CharField(label='Type Descript',max_length=1024, widget=forms.Textarea)
    
class TasksForm(forms.Form):
    name       = forms.CharField(label='Task Name', max_length=100, required=True)
    descript   = forms.CharField(label='Task Descript',max_length=1024, widget=forms.Textarea)
    order      = forms.IntegerField(label='Task Order',required=True, min_value=0, initial=0 )
    typeid     = forms.ModelChoiceField(label='Link to Project Type', queryset=Type.objects.filter(isDeleted=False).all(),required=True)
'''