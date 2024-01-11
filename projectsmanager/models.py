from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

LogNote = [
    ('create','Create'),
    ('edit', 'Edit'),
    ('complete','Completed'),
]

Status = [
    ('open','Open'),
    ('reject', 'Rejected'),
    ('pending', 'Pending'),
    ('complete','Complete'),
]

class User(AbstractUser):
    #login_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
          self.set_password(self.password)
          super().save(*args, **kwargs)
    
class Type(models.Model):
    name        = models.CharField(max_length=200)
    descript    = models.CharField(max_length=1024)    
    def __str__(self):
        return self.name
    
class Priority(models.Model):
    name    = models.CharField(max_length=200)
    level   = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    
    def __str__(self):
        return self.name

class Projects(models.Model):
    name            = models.CharField(max_length=200)
    descript        = models.CharField(max_length=1024)
    status          = models.CharField(max_length=50, choices=Status, default='open')
    completeddate   = models.DateTimeField(null=True, blank=True)
    DueDate         = models.DateTimeField(null=True, blank=True)
    priority        = models.ForeignKey(Priority, on_delete=models.CASCADE)
    type            = models.ForeignKey(Type, on_delete=models.CASCADE)
    staffadd        = models.ForeignKey(User, related_name='project_addedstaff', on_delete=models.CASCADE,null=True, blank=True )
    addeddate       = models.DateTimeField('date published', editable=False, auto_now_add=True)
    staffdelete     = models.ForeignKey(User, related_name='project_deletedstaff', on_delete=models.CASCADE,null=True, blank=True )
    removedate      = models.DateTimeField(null=True, blank=True)
    isDeleted       = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Tasks(models.Model):
    name        = models.CharField(max_length=200)
    descript    = models.CharField(max_length=1024)
    staffadd    = models.ForeignKey(User, related_name='task_addedstaff', on_delete=models.CASCADE,null=True, blank=True )
    addeddate   = models.DateTimeField('date published', editable=False, auto_now_add=True)
    staffdelete = models.ForeignKey(User, related_name='task_deletedstaff', on_delete=models.CASCADE,null=True, blank=True )
    removedate  = models.DateTimeField(null=True, blank=True)
    isDeleted   = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class ProjectsTasks(models.Model):
    tasks       = models.ForeignKey(Tasks, on_delete=models.CASCADE,null=True, blank=True)
    project     = models.ForeignKey(Projects, on_delete=models.CASCADE,null=True, blank=True )
    isDeleted   = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Project: \"{self.project.name}\", Tasks: \"{self.tasks.name} \" "
    
class TaskAssignTo(models.Model):
    tasks       = models.ForeignKey(Tasks, on_delete=models.CASCADE,null=True, blank=True)
    project     = models.ForeignKey(Projects, on_delete=models.CASCADE,null=True, blank=True )
    staffassign = models.ForeignKey(User, related_name='staffassigned', on_delete=models.CASCADE,null=True, blank=True )
    status      = models.CharField(max_length=200, blank=True)
    staffadd    = models.ForeignKey(User, related_name='assigned_addedstaff', on_delete=models.CASCADE,null=True, blank=True )
    addeddate   = models.DateTimeField('date published', editable=False, auto_now_add=True)
    staffdelete = models.ForeignKey(User, related_name='assigned_deletedstaff', on_delete=models.CASCADE,null=True, blank=True )
    removedate  = models.DateTimeField(null=True, blank=True)
    isDeleted   = models.BooleanField(default=False)

    def __str__(self):
        return f"Project: \"{self.project.name}\", Tasks: \"{self.tasks.name} \", Staff: \"{self.staffassign.first_name} {self.staffassign.last_name} \" "
    
class Log(models.Model):
    project     = models.ForeignKey(Projects, on_delete=models.CASCADE,null=True, blank=True )
    task        = models.ForeignKey(Tasks, on_delete=models.CASCADE,null=True, blank=True)
    staff       = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True )
    lognote     = models.CharField(max_length=200, choices=LogNote, default='create')
    addeddate   = models.DateTimeField('date published', editable=False, auto_now_add=True)