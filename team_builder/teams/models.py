from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Skill(models.Model):
    skill_name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.skill_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    fullname = models.CharField(max_length=200, null=True)
    bio = models.TextField(max_length=700, blank=True)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True)
    skills = models.ManyToManyField('Skill', blank=True)

    def __str__(self):
        return self.fullname


# Signal to create a Profile once a User is registered
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Project(models.Model):
    creator = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False, unique=True)
    description = models.TextField(max_length=700, blank=True)
    timeline = models.CharField(max_length=25, null=False)
    requirements = models.TextField(max_length=300, null=False)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Position(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=400, blank=False)
    related_skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Application(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    candidate = models.ForeignKey('Profile', on_delete=models.CASCADE)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    status = models.CharField(default='Waiting response', max_length=18)

    def __str__(self):
        return self.status
