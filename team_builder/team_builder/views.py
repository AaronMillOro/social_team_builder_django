from django.shortcuts import render
from teams import models


def index(request):
    if request.method == 'GET':
        positions = models.Position.objects.all().order_by('name')
        projects = models.Project.objects.all().order_by('title')
        related_skills = models.Position.objects.all().values_list(
            'related_skill_id', flat=True).distinct()
        related_skills = models.Skill.objects.filter(
            id__in=related_skills).order_by('skill_name')
    return render(request, 'index.html', {
        'projects': projects, 'positions': positions,
        'related_skills': related_skills
    })
