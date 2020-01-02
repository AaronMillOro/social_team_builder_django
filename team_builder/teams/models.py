from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Skill(models.Model):
    skill_name = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.skill_name


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True
    )
    fullname = models.CharField(max_length=200, blank=True)
    bio = models.TextField(max_length=400, blank=True)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True)
    skills = models.ManyToManyField('Skill', blank=True)
    current_projects = models.CharField(max_length=20, default='')
    old_projects = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.username


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True, null=False)
    description = models.TextField(max_length=400, blank=True)
    timeline = models.CharField(max_length=25, null=False)
    requirements = models.TextField(max_length=300, null=False)
    finished = models.BooleanField(default=False)
    positions = models.CharField(max_length=75)

    def __str__(self):
        return self.title


class Position(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    project = models.OneToOneField('Project', on_delete=models.CASCADE)
    candidate = models.OneToOneField('Profile', on_delete=models.CASCADE)
    position = models.OneToOneField('Position', on_delete=models.CASCADE)
    status = models.CharField(default='', max_length=2,
        choices=[('a','Accepted'), ('r', 'Rejected')])


# Signal to create a Profile once a User is registered
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
