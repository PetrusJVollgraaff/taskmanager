from django.db import connection
from projectsmanager.models import *

def ShowAllProject():    
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            P.id, 
                            P.name AS 'projectname', 
                            P.descript AS 'projectdescript', 
                            P.addeddate,
                            P.completeddate, 
                            P.DueDate, 
                            PP.name AS 'priorityname', 
                            PP.level, 
                            PT.name AS 'typename', 
                            PT.descript AS 'typedescript'
                        From projectsmanager_projects AS P
                        LEFT JOIN projectsmanager_priority AS PP ON PP.id=P.priority_id
                        LEFT JOIN projectsmanager_type AS PT ON PT.id=P.type_id
                        WHERE P.isDeleted = 0
                    ''')
        row = dictfetchall(cursor)       
        cursor.close()     
        
    return row

def CreatedProject(id):
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            P.id, 
                            P.projectname, 
                            P.projectdescript, 
                            P.completeddate, 
                            P.DueDate, 
                            PP.priorityname, 
                            PP.prioritydescript,
                            PP.level, 
                            PT.typename,  
                            PT.typedescript
                        From projects_project AS P
                        JOIN projects_projectspriority AS PP    ON PP.id=P.projectpriority_id
                        JOIN projects_projectstype AS PT        ON PT.id=P.projecttype_id
                        JOIN projects_projectlog AS PL          ON PL.project_id=P.id
                        WHERE PL.staff_id='''+str(id)+''' AND LOWER(PL.lognote)='create' AND P.isDeleted = 0
                    ''')
        row = dictfetchall(cursor)       
        cursor.close()     
        
    return row

def SignedProject(id):
    
    row = []
    with connection.cursor() as cursor:
        cursor.execute(''' 
                    SELECT 
                        P.id, 
                        P.name AS 'projectname', 
                        P.descript AS 'projectdescript', 
                        P.addeddate,
                        P.completeddate, 
                        P.DueDate, 
                        PP.name AS 'priorityname', 
                        PP.level, 
                        PT.name AS 'typename',  
                        PT.descript AS 'typedescript'
                    From projectsmanager_taskassignto AS AT
                    
                    JOIN projectsmanager_projects AS P  ON P.id = AT.project_id
                    JOIN projectsmanager_priority AS PP ON PP.id = P.priority_id
                    JOIN projectsmanager_type AS PT     ON PT.id = P.type_id
                    JOIN projectsmanager_tasks AS T     ON T.id = AT.tasks_id
                    
                    WHERE AT.staffassign_id='''+str(id)+''' AND AT.status!='complete' 
                    AND AT.id = (
                        SELECT 
                            AT2.id
                        FROM projectsmanager_taskassignto AS AT2
                        JOIN projectsmanager_tasks AS T2 ON T2.id = AT2.tasks_id
                        WHERE AT2.project_id=P.id
                        ORDER BY AT2.addeddate ASC LIMIT 1
                    ) AND P.isDeleted = 0
                    ORDER BY AT.addeddate DESC
                ''')
        row = dictfetchall(cursor)
        cursor.close()       
    return row

def SignedProjectHistory(id):   
    row = []
    with connection.cursor() as cursor:
        cursor.execute(''' 
                    SELECT 
                        P.id, 
                        P.projectname, 
                        P.projectdescript, 
                        P.startingdate, 
                        P.completeddate, 
                        P.DueDate, 
                        PP.priorityname, 
                        PT.typename, 
                        PP.prioritydescript, 
                        PT.typedescript, 
                        AT.staff_id, 
                        T.tasksorder
                    From projects_assignedto AS AT
                    JOIN projects_project AS P              ON P.id=AT.project_id
                    JOIN projects_projectspriority AS PP    ON PP.id=P.projectpriority_id
                    JOIN projects_projectstype AS PT        ON PT.id=P.projecttype_id
                    JOIN projects_tasks AS T                ON T.id=AT.tasks_id
                    WHERE AT.staff_id='''+str(id)+''' AND AT.status=='complete'
                    ORDER BY T.tasksorder, AT.addeddate DESC
                ''')
        row = dictfetchall(cursor)
        cursor.close()       
    return row

def ProjectDetails(id):
    row = []
    with connection.cursor() as cursor:
        cursor.execute(''' 
                        ;WITH STAFF AS(
                            SELECT 
                                U.id AS userid, 
                                U.first_name +' '+ U.last_name AS staffname, 
                                AT.project_id, 
                                AT.tasks_id
                            FROM projectsmanager_user AS U
                            JOIN projectsmanager_taskassignto AS AT ON AT.staffassign_id = U.id 
                            WHERE AT.project_id= '''+ str(id) +'''
                            ORDER BY AT.addeddate DESC
                        ),

                        Tasks AS (
                            SELECT AT.project_id ,
                                json_group_array(json_object( 
                                        'id', T.id,
                                        'name', T.name, 
                                        'descript', T.descript, 
                                        'status', AT.status,
                                        'staffid', S.userid,
                                        'staffname', S.staffname
                                
                                )) AS Task
                            FROM projectsmanager_taskassignto AS AT 
                            JOIN projectsmanager_tasks AS T ON T.id = AT.tasks_id
                            JOIN STAFF AS S          ON S.project_id = AT.project_id AND S.tasks_id = AT.id
                            WHERE AT.project_id = '''+ str(id) +'''
                        )
                    
                        SELECT 
                        P.id, 
                        P.name AS projectname, 
                        P.descript AS projectdescript, 
                        P.addeddate, 
                        P.completeddate, 
                        P.DueDate, 
                        PP.name AS priorityname,
                        COALESCE(T.Task, '[]') AS Task
                        --,PT.name AS typename, 
                        --PT.descript AS typedescript                 
                    From projectsmanager_projects AS P
                    LEFT JOIN projectsmanager_priority AS PP ON PP.id=P.priority_id
                    --LEFT JOIN projectsmanager_type AS PT     ON PT.id=P.type_id
                    LEFT JOIN Tasks AS T                     ON T.project_id = P.id
                    WHERE P.id='''+ str(id) +'''
                    ''')
        row = dictfetchall(cursor)       
        cursor.close() 
        
        #row = getAssignedTasks(row)     
    return row

def getAssignedTasks(project_row):
    if project_row and isinstance(project_row, list):   
        for i,each in enumerate(project_row):
            with connection.cursor() as cursor:
                project_id = str(each.get("id"))
                cursor.execute('''
                                ;WITH STAFF AS(
                                    SELECT 
                                        U.id AS userid, 
                                        U.first_name AS firstname, 
                                        U.last_name AS lastname, 
                                        AT.project_id, 
                                        AT.tasks_id
                                    FROM projects_user AS U
                                    JOIN projects_assignedto AS AT ON AT.staff_id=U.id 
                                    WHERE AT.project_id='''+ project_id +''' 
                                    ORDER BY AT.addeddate DESC
                                ),

                                
                               
                               Select 
                               AT.id AS assignedid, 
                               T.tasksname, 
                               T.tasksdescript, 
                               T.id AS taskid, 
                               AT.status,
                               S.userid,
                               S.firstname,
                               S.lastname
                               FROM projects_assignedto AS AT 
                               JOIN projects_tasks AS T ON T.id = AT.tasks_id
                               JOIN STAFF AS S          ON S.project_id = AT.project_id AND S.tasks_id = AT.id
                               WHERE AT.project_id='''+project_id+''' ''')                           
                project_row[i]["tasks"] = dictfetchall(cursor)                
                cursor.close()                

    return project_row

def getTasks(id):
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            T.id, 
                            T.tasksname, 
                            T.tasksdescript                  
                        From projects_tasks AS T
                        WHERE T.projecttype_id='''+str(id)+'''
                    ''')
        row = dictfetchall(cursor)       
        cursor.close()      
    return row

def getStaff():
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            U.id, 
                            U.first_name, 
                            U.last_name                  
                        From projectsmanager_user AS U
                        WHERE U.id != 1
                    ''')
        row = dictfetchall(cursor)       
        cursor.close()      
    return row

def UpdateLog(projectid, staffid, current_date):
    
    staffcreate = User.objects.get(id = staffid)
    projectC    = Projects.objects.get(id = projectid)
    projectlog  = Log(lognote="deleted", project=projectC, staff=staffcreate, addeddate=current_date)
    projectlog.save()

def getPriorities():
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            PP.id, 
                            PP.name, 
                            PP.level                  
                        From projectsmanager_priority AS PP 
                        ORDER BY PP.level
                    ''')
        row = dictfetchall(cursor)       
        cursor.close()      
    return row

def getTypes():
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT 
                            PT.id, 
                            PT.name, 
                            PT.descript  
                        From projectsmanager_type AS PT
                    ''')
        row = dictfetchall(cursor)       
        cursor.close()      
    return row

def getAllTasks():
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
                    SELECT 
                        T.id, 
                        T.tasksname, 
                        T.tasksdescript, 
                        T.tasksorder, 
                        PT.typename                  
                    From projects_tasks AS T
                    JOIN projects_projectstype AS PT ON PT.id = T.projecttype_id
                    WHERE T.isDeleted = 0 AND T.deleteddate IS NULL''')
        row = dictfetchall(cursor)       
        cursor.close()      
    return row
    
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
def dictChoices(choices):
    test = list()
    for i,each in enumerate(choices):
        dictz = {'value': each[0], 'name': each[1]}
        test.append(dictz)
        
    return test
