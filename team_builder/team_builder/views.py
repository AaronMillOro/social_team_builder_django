from django.shortcuts import render
from teams import models


def index(request):
    if request.method == 'GET':
        positions = models.Position.objects.all().order_by('name')
        projects = models.Project.objects.all().order_by('title')
    return render(request, 'index.html', {
        'projects': projects, 'positions': positions}
    )
