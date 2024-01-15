from django.db import connection
from projectsmanager.models import *

def ShowAllProject():    
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
                        ;WITH Staff AS(
                            SELECT 
                                P.id as projectid,
                                U.id AS userid, 
                                CASE 
                                    WHEN (U.first_name IS NULL OR U.first_name = '') AND (U.last_name IS NULL OR U.last_name = '') THEN
                                        U.username
                                    ELSE
                                        U.first_name ||' '|| U.last_name
                                END AS staffname
                            FROM projectsmanager_projects AS P
                            JOIN projectsmanager_user AS U ON P.staffadd_id = U.id  
                            WHERE P.isDeleted = 0
                        ),
                       
                        EditProject AS (
                            SELECT
                                P.id,
                                CASE 
                                    WHEN EXISTS( SELECT PP.mainproject_id FROM projectsmanager_projectprojects PP WHERE PP.mainproject_id = P.id  ) THEN
                                        (SELECT
                                            P1.id 
                                        FROM projectsmanager_projects P1 
                                        JOIN projectsmanager_projectprojects PP             
                                        WHERE  PP.mainproject_id = P1.id
                                        ORDER BY PP.editeddate DESC LIMIT 1
                                        )
                                    ELSE
                                        P.id
                                END AS projectid,
                                CASE 
                                    WHEN EXISTS( SELECT PP.mainproject_id FROM projectsmanager_projectprojects PP WHERE PP.mainproject_id = P.id  ) THEN
                                        1
                                    ELSE
                                        0
                                END AS subproject
                            FROM projectsmanager_projects P
                            WHERE P.isDeleted = 0    
                        ),

                        ProjectDetails AS (
                            SELECT     
                                P.id,
                                (SELECT P1.name 
                                FROM projectsmanager_projects P1 
                                WHERE  P1.id = EP.projectid) AS 'projectname', 
                                (SELECT P1.descript 
                                FROM projectsmanager_projects P1 
                                WHERE  P1.id = EP.projectid) AS 'projectdescript',
                                EP.subproject
                            FROM projectsmanager_projects P
                            JOIN EditProject AS EP ON EP.id = P.id
                            WHERE P.isDeleted = 0
                        )             
                       
                        SELECT 
                            P.id, 
                            PD.projectname, 
                            PD.projectdescript, 
                            strftime('%d/%m/%Y %H:%M', P.addeddate) AS addeddate,
                            P.completeddate, 
                            P.DueDate, 
                            PP.name AS 'priorityname', 
                            PP.level, 
                            PT.name AS 'typename', 
                            PT.descript AS 'typedescript',
                            S.staffname  
                        FROM projectsmanager_projects P
                        JOIN ProjectDetails AS PD                   ON PD.id = P.id 
                        LEFT JOIN projectsmanager_priority AS PP    ON PP.id=P.priority_id
                        LEFT JOIN projectsmanager_type AS PT        ON PT.id=P.type_id
                        LEFT JOIN Staff AS S                        ON S.projectid = P.id 
                        WHERE P.isDeleted = 0
                    ''')
        row = dictfetchall(cursor)       
        cursor.close()     
        
    return row

def MyProject(userid):    
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
                        ;WITH Staff AS(
                            SELECT 
                                P.id as projectid,
                                U.id AS userid, 
                                CASE 
                                    WHEN (U.first_name IS NULL OR U.first_name = '') AND (U.last_name IS NULL OR U.last_name = '') THEN
                                        U.username
                                    ELSE
                                        U.first_name ||' '|| U.last_name
                                END AS staffname
                            FROM projectsmanager_projects AS P
                            JOIN projectsmanager_user AS U ON P.staffadd_id = U.id  
                            WHERE P.isDeleted = 0
                        ),
                       
                        EditProject AS (
                            SELECT
                                P.id,
                                CASE 
                                    WHEN EXISTS( SELECT PP.mainproject_id FROM projectsmanager_projectprojects PP WHERE PP.mainproject_id = P.id  ) THEN
                                        (SELECT
                                            P1.id 
                                        FROM projectsmanager_projects P1 
                                        JOIN projectsmanager_projectprojects PP             
                                        WHERE  PP.mainproject_id = P1.id
                                        ORDER BY PP.editeddate DESC LIMIT 1
                                        )
                                    ELSE
                                        P.id
                                END AS projectid,
                                CASE 
                                    WHEN EXISTS( SELECT PP.mainproject_id FROM projectsmanager_projectprojects PP WHERE PP.mainproject_id = P.id  ) THEN
                                        1
                                    ELSE
                                        0
                                END AS subproject
                            FROM projectsmanager_projects P
                            WHERE P.isDeleted = 0    
                        ),

                        ProjectDetails AS (
                            SELECT     
                                P.id,
                                (SELECT P1.name 
                                FROM projectsmanager_projects P1 
                                WHERE  P1.id = EP.projectid) AS 'projectname', 
                                (SELECT P1.descript 
                                FROM projectsmanager_projects P1 
                                WHERE  P1.id = EP.projectid) AS 'projectdescript',
                                EP.subproject
                            FROM projectsmanager_projects P
                            JOIN EditProject AS EP ON EP.id = P.id
                            WHERE P.isDeleted = 0 AND P.staffadd_id = '''+str(userid)+'''
                        )
                       
                        SELECT 
                            P.id, 
                            PD.projectname, 
                            PD.projectdescript, 
                            strftime('%d/%m/%Y %H:%M', P.addeddate) AS addeddate,
                            P.completeddate, 
                            P.DueDate, 
                            PP.name AS 'priorityname', 
                            PP.level, 
                            PT.name AS 'typename', 
                            PT.descript AS 'typedescript',
                            S.staffname  
                        FROM projectsmanager_projects P
                        JOIN ProjectDetails AS PD                   ON PD.id = P.id 
                        LEFT JOIN projectsmanager_priority AS PP    ON PP.id=P.priority_id
                        LEFT JOIN projectsmanager_type AS PT        ON PT.id=P.type_id
                        LEFT JOIN Staff AS S                        ON S.projectid = P.id 
                        WHERE P.isDeleted = 0 AND P.staffadd_id = '''+str(userid)+'''
                    ''')
        row = dictfetchall(cursor)       
        cursor.close()     
        
    return row

def SignedProject(id):
    
    row = []
    with connection.cursor() as cursor:
        cursor.execute(''' 
                    ;WITH Staff AS(
                        SELECT 
                            P.id as projectid,
                            U.id AS userid, 
                            CASE 
                                WHEN (U.first_name IS NULL OR U.first_name = '') AND (U.last_name IS NULL OR U.last_name = '') THEN
                                    U.username
                                ELSE
                                    U.first_name ||' '|| U.last_name
                            END AS staffname
                        FROM projectsmanager_projects AS P
                        JOIN projectsmanager_user AS U ON P.staffadd_id = U.id  
                        WHERE P.isDeleted = 0
                    ),
                       
                    EditProject AS (
                            SELECT
                                P.id,
                                CASE 
                                    WHEN EXISTS( SELECT PP.mainproject_id FROM projectsmanager_projectprojects PP WHERE PP.mainproject_id = P.id  ) THEN
                                        (SELECT
                                            P1.id 
                                        FROM projectsmanager_projects P1 
                                        JOIN projectsmanager_projectprojects PP             
                                        WHERE  PP.mainproject_id = P1.id
                                        ORDER BY PP.editeddate DESC LIMIT 1
                                        )
                                    ELSE
                                        P.id
                                END AS projectid,
                                CASE 
                                    WHEN EXISTS( SELECT PP.mainproject_id FROM projectsmanager_projectprojects PP WHERE PP.mainproject_id = P.id  ) THEN
                                        1
                                    ELSE
                                        0
                                END AS subproject
                            FROM projectsmanager_projects P
                            WHERE P.isDeleted = 0    
                        ),

                        ProjectDetails AS (
                            SELECT     
                                P.id,
                                (SELECT P1.name 
                                FROM projectsmanager_projects P1 
                                WHERE  P1.id = EP.projectid) AS 'projectname', 
                                (SELECT P1.descript 
                                FROM projectsmanager_projects P1 
                                WHERE  P1.id = EP.projectid) AS 'projectdescript',
                                EP.subproject
                            FROM projectsmanager_projects P
                            JOIN EditProject AS EP ON EP.id = P.id
                            WHERE P.isDeleted = 0
                        )
                         
                    SELECT 
                        P.id, 
                        PD.projectname, 
                        PD.projectdescript,
                        strftime('%d/%m/%Y %H:%M', P.addeddate) AS addeddate,
                        P.completeddate, 
                        P.DueDate, 
                        PP.name AS 'priorityname', 
                        PP.level, 
                        PT.name AS 'typename',  
                        PT.descript AS 'typedescript',
                        S.staffname,
                        P.staffadd_id
                    From projectsmanager_taskassignto AS AT
                    JOIN ProjectDetails AS PD                   ON PD.id = P.id 
                    JOIN projectsmanager_projects AS P  ON P.id = AT.project_id
                    JOIN projectsmanager_priority AS PP ON PP.id = P.priority_id
                    JOIN projectsmanager_type AS PT     ON PT.id = P.type_id
                    JOIN Staff AS S                     ON S.projectid = P.id
                    
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

def ProjectDetails(id):
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
                    ; WITH EditProject AS (
                            SELECT
                                P.id,
                                CASE 
                                    WHEN EXISTS( SELECT PP.mainproject_id FROM projectsmanager_projectprojects PP WHERE PP.mainproject_id = P.id  ) THEN
                                        (SELECT
                                            P1.id 
                                        FROM projectsmanager_projects P1 
                                        JOIN projectsmanager_projectprojects PP             
                                        WHERE  PP.mainproject_id = P1.id
                                        ORDER BY PP.editeddate DESC LIMIT 1
                                        )
                                    ELSE
                                        P.id
                                END AS projectid,
                                CASE 
                                    WHEN EXISTS( SELECT PP.mainproject_id FROM projectsmanager_projectprojects PP WHERE PP.mainproject_id = P.id  ) THEN
                                        1
                                    ELSE
                                        0
                                END AS subproject
                            FROM projectsmanager_projects P
                            WHERE P.isDeleted = 0    
                        ),

                        ProjectDetails AS (
                            SELECT     
                                P.id,
                                (SELECT P1.name 
                                FROM projectsmanager_projects P1 
                                WHERE  P1.id = EP.projectid) AS 'projectname', 
                                (SELECT P1.descript 
                                FROM projectsmanager_projects P1 
                                WHERE  P1.id = EP.projectid) AS 'projectdescript',
                                EP.subproject
                            FROM projectsmanager_projects P
                            JOIN EditProject AS EP ON EP.id = P.id
                            WHERE P.isDeleted = 0 AND P.id='''+ str(id) +'''
                        )   

                    SELECT 
                        P.id, 
                        PD.projectname, 
                        PD.projectdescript, 
                        P.addeddate, 
                        P.completeddate, 
                        P.DueDate, 
                        PP.name AS priorityname
                        --COALESCE(T.Task, '[]') AS Task
                        ,PT.name AS typename, 
                        PT.descript AS typedescript ,
                        U.first_name +' '+ U.last_name AS staffname,
                        CASE
                            WHEN EXISTS(
                                SELECT *
                                FROM projectsmanager_taskassignto AS AT 
                                WHERE AT.project_id = P.id AND AT.status != 'complete' AND AT.isDeleted = 0
                            ) OR P.status = 'complete' THEN 0
                            ELSE 1
                        END AS 'completebtn'               
                    From projectsmanager_projects AS P
                    JOIN ProjectDetails AS PD           ON PD.id = P.id 
                    JOIN projectsmanager_priority AS PP ON PP.id = P.priority_id
                    JOIN projectsmanager_type AS PT     ON PT.id = P.type_id
                    JOIN projectsmanager_user AS U      ON P.staffadd_id = U.id 
                    WHERE P.id='''+ str(id) +''' AND P.isDeleted = 0
                    ''')
        row = dictfetchall(cursor)       
        cursor.close() 
        
        row = getAssignedTasks(row, str(id))     
    return row

def ProjectEditDetails(id):
    row = []
    with connection.cursor() as cursor:
        cursor.execute('''
                    ; WITH EditProject AS (
                            SELECT
                                P.id,
                                CASE 
                                    WHEN EXISTS( SELECT PP.mainproject_id FROM projectsmanager_projectprojects PP WHERE PP.mainproject_id = P.id  ) THEN
                                        (SELECT
                                            P1.id 
                                        FROM projectsmanager_projects P1 
                                        JOIN projectsmanager_projectprojects PP             
                                        WHERE  PP.mainproject_id = P1.id
                                        ORDER BY PP.editeddate DESC LIMIT 1
                                        )
                                    ELSE
                                        P.id
                                END AS projectid,
                                CASE 
                                    WHEN EXISTS( SELECT PP.mainproject_id FROM projectsmanager_projectprojects PP WHERE PP.mainproject_id = P.id  ) THEN
                                        1
                                    ELSE
                                        0
                                END AS subproject
                            FROM projectsmanager_projects P
                            WHERE P.isDeleted = 0    
                        ),

                        ProjectDetails AS (
                            SELECT     
                                P.id,
                                (SELECT P1.name 
                                FROM projectsmanager_projects P1 
                                WHERE  P1.id = EP.projectid) AS 'projectname', 
                                (SELECT P1.descript 
                                FROM projectsmanager_projects P1 
                                WHERE  P1.id = EP.projectid) AS 'projectdescript',
                                EP.subproject
                            FROM projectsmanager_projects P
                            JOIN EditProject AS EP ON EP.id = P.id
                            WHERE P.isDeleted = 0 AND P.id='''+ str(id) +'''
                        )   

                    SELECT 
                        P.id, 
                        PD.projectname AS 'name', 
                        PD.projectdescript AS 'descript', 
                        P.DueDate, 
                        PP.id AS 'priority'
                        --COALESCE(T.Task, '[]') AS tasks
                        ,PT.id AS 'type'
                    From projectsmanager_projects AS P
                    JOIN ProjectDetails AS PD           ON PD.id = P.id 
                    JOIN projectsmanager_priority AS PP ON PP.id = P.priority_id
                    JOIN projectsmanager_type AS PT     ON PT.id = P.type_id
                    WHERE P.id='''+ str(id) +''' AND P.isDeleted = 0
                    ''')
        row = dictfetchall(cursor)       
        cursor.close() 
        
        row = getAssignedTasks(row, str(id))     
    return row



def getAssignedTasks(project_row, project_id):
    if project_row and isinstance(project_row, list):   
        for i,each in enumerate(project_row):
            with connection.cursor() as cursor:
                cursor.execute('''
                            ;WITH STAFF AS(
                                SELECT 
                                    U.id AS userid, 
                                    CASE 
                                        WHEN (U.first_name IS NULL OR U.first_name = '') AND (U.last_name IS NULL OR U.last_name = '') THEN
                                            U.username
                                        ELSE
                                            U.first_name ||' '|| U.last_name
                                    END AS staffname,
                                    AT.project_id, 
                                    AT.tasks_id
                                FROM projectsmanager_user AS U
                                JOIN projectsmanager_taskassignto AS AT ON AT.staffassign_id = U.id 
                                WHERE AT.project_id= '''+ project_id +'''
                                ORDER BY AT.addeddate DESC
                            )
   
                            SELECT 
                                T.id AS id, 
                                T.name, 
                                T.descript, 
                                AT.status,
                                S.userid,
                                S.staffname
                            FROM projectsmanager_taskassignto AS AT 
                            LEFT JOIN projectsmanager_tasks AS T ON T.id = AT.tasks_id
                            LEFT JOIN STAFF AS S          ON S.project_id = AT.project_id AND S.tasks_id = AT.id
                            WHERE AT.project_id = '''+ project_id +'''
                        ''')                           
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
                            CASE 
                                WHEN (U.first_name IS NULL OR U.first_name = '') AND (U.last_name IS NULL OR U.last_name = '') THEN
                                    U.username
                                ELSE
                                    U.first_name ||' '|| U.last_name
                            END AS staffname                
                        From projectsmanager_user AS U
                        WHERE U.id != 1
                    ''')
        row = dictfetchall(cursor)       
        cursor.close()      
    return row

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
    
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
