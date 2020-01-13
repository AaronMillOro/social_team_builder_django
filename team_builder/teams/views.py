from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from . import models
from . import forms


# ---- Sign Up, Sign In and Sign Out logic -------
def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(request, "You're now a user! ")
            return HttpResponseRedirect(
                reverse('teams:profile_edit'))
    return render(request, 'signup.html', {'form': form})


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('index'))
                else:
                    messages.error(
                        request, "That user account has been disabled.")
            else:
                messages.error(
                    request, "Username or password is incorrect.")
    return render(request, 'signin.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('index'))


# ---- Profile logic -------
def creator_profile(request, pk):
    profile = get_object_or_404(models.Profile, pk=pk)
    positions = models.Position.objects.filter(
        project_id__creator=profile.id).order_by('name')
    old_projects = models.Project.objects.only(
        'creator', 'finished').filter(
        creator=profile.id, finished=True).order_by('title')
    current_projects = models.Project.objects.only(
        'creator', 'finished').filter(
        creator=profile.id, finished=False).order_by('title')
    return render(request, 'profile.html', {
        'profile': profile, 'old_projects': old_projects,
        'positions': positions, 'current_projects': current_projects}
    )


@login_required
def profile(request):
    if request.method == 'GET':
        profile = request.user.profile
        positions = models.Position.objects.filter(
            project_id__creator=request.user.id).order_by('name')
        old_projects = models.Project.objects.only(
            'creator', 'finished').filter(
            creator=request.user.id, finished=True).order_by('title')
        current_projects = models.Project.objects.only(
            'creator', 'finished').filter(
            creator=request.user.id, finished=False).order_by('title')
    return render(request, 'profile.html', {
        'profile': profile, 'old_projects': old_projects,
        'positions': positions, 'current_projects': current_projects}
    )


@login_required
@transaction.atomic
def profile_edit(request):
    try:
        profile_form = forms.ProfileForm(instance=request.user.profile)
        skills_form = forms.SkillsForm(instance=request.user.profile)
        if request.method == 'POST':
            profile_form = forms.ProfileForm(
                request.POST, request.FILES, instance=request.user.profile
            )
            skills_form = forms.SkillsForm(
                request.POST, instance=request.user.profile
            )
            if profile_form.is_valid() or skills_form.is_valid():
                profile_form.save()
                skills_form.save()
                messages.success(request, 'Profile successfully updated!')
                return redirect(reverse('teams:profile'))
    except ValueError:
        messages.error(request, 'Check the form data!')
    return render(
        request, 'profile_edit.html', {
            'profile_form': profile_form, 'skills_form': skills_form,}
    )


@login_required
def add_skills(request):
    """ View to render skills from database and to add a new skill """
    if request.method == 'POST':
        new_skill_form = forms.NewSkillForm(request.POST)
        if new_skill_form.is_valid():
            new_skill_form.save()
            messages.success(request, 'New skill added to database!')
            return redirect('teams:add_skills')
    else:
        skills = models.Skill.objects.all()
        skills = skills.extra(order_by = ['skill_name'])
        new_skill_form = forms.NewSkillForm()
    return render(request, 'add_skills.html', {
        'skills': skills, 'new_skill_form': new_skill_form,}
    )


# ---- Projects logic: Create, Read, Delete ----
@login_required
def my_projects(request):
    if request.method == 'GET':
        positions = models.Position.objects.filter(
            project_id__creator=request.user.id).order_by('name')
        projects = models.Project.objects.filter(
            creator=request.user.id).order_by('title')
    return render(request, 'projects.html', {
        'projects': projects, 'positions': positions}
    )


@login_required
@transaction.atomic
def create_project(request):
    """ View to create a Project with its required positions """
    try:
        form_a = forms.ProjectFormPartA()
        form_b = forms.ProjectFormPartB()
        formset = forms.PositionFormSet(
            queryset=models.Project.objects.none()
        )
        if request.method == 'POST':
            form_a = forms.ProjectFormPartA(request.POST)
            form_b = forms.ProjectFormPartB(request.POST)
            formset = forms.PositionFormSet(request.POST)
            if form_a.is_valid() and form_b.is_valid():
                project = form_b.save(commit=False) #fills timeline and needs
                project.creator = models.Profile.objects.get(
                    pk=request.user.id
                )
                project.title = form_a.cleaned_data['title']
                project.description = form_a.cleaned_data['description']
                if formset.is_valid():
                    project.save() # save project instance
                    for position in formset:
                        if position.cleaned_data != {}: #No empty instances
                            position = position.save(commit=False)
                            position.project = project
                            position.save()
                    messages.success(request, 'New project created!')
                    return HttpResponseRedirect(reverse('teams:my_projects'))
    except ValueError:
        messages.error(request, 'Check the form data!')
    return render(request, 'project_create.html', {
        'form_a': form_a, 'form_b': form_b, 'formset': formset,}
    )


def project_details(request, pk):
    """Display details of a project and the positions of it"""
    project = get_object_or_404(models.Project, pk=pk)
    positions = models.Position.objects.filter(
        project=project.id).order_by('name')
    # logic to apply for an available position
    if request.user.is_authenticated:
        if request.method == 'POST':
            position_id = request.POST.get('position_id')
            position = get_object_or_404(models.Position, pk=position_id)
            profile = request.user.profile
            application = models.Application(project=project,
                position=position, candidate=profile
            )
            application.save(force_insert=True)
            messages.success(request, 'Your application was sent')
            return HttpResponseRedirect(reverse('teams:applications'))
    return render(request, 'project_details.html', {
        'project':project, 'positions':positions,
        }
    )


@login_required
def project_delete(request, pk):
    """Ask user to delete a previously created project"""
    project = get_object_or_404(models.Project, pk=pk)
    if request.method == 'POST':
        models.Application.objects.filter(project=project.id).delete()
        models.Position.objects.filter(project=project.id).delete()
        models.Project.objects.filter(id=pk).delete()
        messages.success(request, 'Project was deleted T_T ')
        return HttpResponseRedirect(reverse('teams:my_projects'))
    return render(request, 'project_delete.html',
        {'project': project, }
    )


def project_finish(request, pk):
    """Ask user to set a project as finished"""
    project = get_object_or_404(models.Project, pk=pk)
    if request.method == 'POST':
        #project = models.Project.objects.get(pk=pk)
        project.finished = True
        project.save()
        messages.success(request, 'Project was finished!')
        return HttpResponseRedirect(reverse('teams:my_projects'))
    return render(request, 'project_finish.html',
        {'project': project, }
    )


def projects_search(request):
    """Get the projects from a query search (term)"""
    term = request.GET.get('query')
    projects_query = models.Project.objects.only(
        'title','description').order_by('title').filter(
        Q(title__icontains=term)|Q(description__icontains=term))
    positions = models.Position.objects.only('project','name').order_by(
        'name').filter(Q(project__in=projects_query))
    return render(request,'projects_search.html', {
        'projects_query': projects_query, 'positions': positions,
    })


def projects_skill(request, skill):
    """Get the projects with a selected skill"""
    skill_name = models.Skill.objects.get(pk=skill)
    positions = models.Position.objects.only('related_skill',
        'name').order_by('name').filter(Q(related_skill_id=skill))

    projects_query = models.Position.objects.values_list(
        'project_id', flat=True).filter(
        Q(related_skill_id=skill)).distinct()
    projects_query = models.Project.objects.filter(
        id__in=projects_query).order_by('title')

    return render(request,'projects_skill.html', {
        'projects_query': projects_query,
        'positions': positions, 'skill_name': skill_name,
    })


# ---- Applications logic ----
@login_required
def applications(request):
    """
    View that gestionates applications to user projects and
    the applications made by the user
    """
    my_candidatures = models.Application.objects.filter(
        candidate_id=request.user.profile).order_by('position')
    applications = models.Application.objects.filter(
        project_id__creator=request.user.profile).order_by('position')
    return render(
        request, 'applications.html', {
        'applications': applications, 'my_candidatures':my_candidatures,
        }
    )


@login_required
def application_decision(request, pk):
    """ User takes the decision of a given application """
    application = get_object_or_404(models.Application, pk=pk)
    profile = get_object_or_404(models.Profile, pk=application.candidate.id)
    application_form = forms.ApplicationForm(instance=application)
    if request.method == 'POST':
        application_form = forms.ApplicationForm(
            request.POST, instance=application
        )
        if application_form.is_valid():
            application_form.save() # save decision
            application = get_object_or_404(models.Application, pk=pk)
            if application.status == 'Accepted':
                # The position will not be longer available
                position = models.Position.objects.get(
                    pk=application.position.id
                )
                position.available = False
                position.save()
                # The other candidates will be rejected by default
                applications = models.Application.objects.filter(
                    position=position).exclude(candidate=application.candidate
                )
                applications.update(status='Rejected')
            messages.success(request, 'Decision made! A notification was sent')
            return HttpResponseRedirect(reverse('teams:applications'))
    return render(request, 'application_decision.html', {
        'application': application, 'application_form':application_form,
        'profile':profile,
        }
    )
