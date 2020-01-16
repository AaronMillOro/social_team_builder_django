from django.shortcuts import render
from teams import models


def index(request):
    if request.method == 'GET':
        projects = models.Project.objects.filter(
            finished=False).order_by('title')
        positions = models.Position.objects.filter(
            project__in=projects).order_by('name')
        related_skills = models.Position.objects.filter(
            project__in=projects).values_list(
            'related_skill_id', flat=True).distinct()
        related_skills = models.Skill.objects.filter(
            id__in=related_skills).order_by('skill_name')
    return render(request, 'index.html', {
        'projects': projects, 'positions': positions,
        'related_skills': related_skills}
    )
