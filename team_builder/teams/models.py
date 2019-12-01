from django.db import models
from django.contrib.auth.models import User

# todo: change to a new model to add from users the different skills
SKILLS = [
    ('1', 'HTML/CSS'),
    ('2', 'Wordpress'),
    ('3', 'JavaScript'),
    ('4', 'Ruby'),
    ('5', 'Django'),
    ('6', 'GOlang')
]


class Profile(models.Model):
    username = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True
    )
    bio = models.TextField(max_length=400, blank=True)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True)
    skills = models.CharField(max_length=30, choices=SKILLS, default='')
    current_projects = models.CharField(max_length=20, default='')
    old_projects = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.username


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True, null=False)
    timeline = models.CharField(max_length=25, null=False)
    requirements = models.CharField(max_length=255, null=False)
    finished = models.BooleanField(default=False)
    positions = models.CharField(max_length=75)

    def __str__(self):
        return self.title


class Application(models.Model):
    project = models.OneToOneField('Project', on_delete=models.CASCADE)
    candidate = models.OneToOneField('Profile', on_delete=models.CASCADE)
    position = models.OneToOneField('Position', on_delete=models.CASCADE)
    status = models.CharField(default='', max_length=2,
        choices=[('a','Accepted'), ('r', 'Rejected')])


class Position(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
