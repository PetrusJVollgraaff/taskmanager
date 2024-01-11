# Generated by Django 4.1 on 2024-01-11 10:13

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('level', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=1024)),
                ('status', models.CharField(choices=[('open', 'Open'), ('reject', 'Rejected'), ('pending', 'Pending'), ('complete', 'Complete')], default='open', max_length=50)),
                ('completeddate', models.DateTimeField(blank=True, null=True)),
                ('DueDate', models.DateTimeField(blank=True, null=True)),
                ('addeddate', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('removedate', models.DateTimeField(blank=True, null=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectsmanager.priority')),
                ('staffadd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_addedstaff', to=settings.AUTH_USER_MODEL)),
                ('staffdelete', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_deletedstaff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('descript', models.CharField(max_length=1024)),
                ('addeddate', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('removedate', models.DateTimeField(blank=True, null=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('staffadd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_addedstaff', to=settings.AUTH_USER_MODEL)),
                ('staffdelete', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_deletedstaff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskAssignTo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=200)),
                ('addeddate', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('removedate', models.DateTimeField(blank=True, null=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectsmanager.projects')),
                ('staffadd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_addedstaff', to=settings.AUTH_USER_MODEL)),
                ('staffassign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staffassigned', to=settings.AUTH_USER_MODEL)),
                ('staffdelete', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_deletedstaff', to=settings.AUTH_USER_MODEL)),
                ('tasks', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectsmanager.tasks')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectsTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isDeleted', models.BooleanField(default=False)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectsmanager.projects')),
                ('tasks', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectsmanager.tasks')),
            ],
        ),
        migrations.AddField(
            model_name='projects',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectsmanager.type'),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lognote', models.CharField(choices=[('create', 'Create'), ('edit', 'Edit'), ('complete', 'Completed')], default='create', max_length=200)),
                ('addeddate', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectsmanager.projects')),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectsmanager.tasks')),
            ],
        ),
    ]
