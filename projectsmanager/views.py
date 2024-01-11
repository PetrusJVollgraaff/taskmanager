from django.shortcuts import render
from .models import *
from .SQL import *
from .functions import *

# Create your views here.

def index(request):
    user            = request.user
    projectz        = SignedProject(user.id) if user.is_authenticated else ShowAllProject()
    displayby       = CheckCookie(request)
    displaytitle    = {"priority": "Priority", "type": "Type"}.get(displayby, "Create Date")
    orderbyz        = {"priority": "level", "type": "typename"}.get(displayby, "addeddate")
    
    print( projectz )

    projectz.sort(key = lambda x:x[orderbyz])
    return render(request, "projects/main.html",{"projects": projectz, "displayby": displaytitle})


