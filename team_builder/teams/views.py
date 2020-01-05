from django.db import transaction
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
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
                        reverse('teams:profile'))
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
@login_required
def profile(request):
    if request.method == 'GET':
        #applications = request.applications
        #positions = request.positions
        profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})


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


# ---- Projects logic: CRUD (Create, Read, Update, Delete) ----
@login_required
def my_projects(request):
    if request.method == 'GET':
        #applications = request.applications
        #positions = request.positions
        projects = models.Project.objects.filter(creator=request.user.id)
    return render(request, 'projects.html', {'projects': projects})


@login_required
def create_project(request):

    try:
        form_a = forms.ProjectFormPartA()
        form_b = forms.ProjectFormPartB()
        formset = forms.PositionFormSet()

        if request.method == 'POST':
            form_a = forms.ProjectFormPartA(request.POST)
            form_b = forms.ProjectFormPartB(request.POST)
            formset = forms.PositionFormSet(request.POST)

            if form_a.is_valid() and form_b.is_valid():
                project = form_b.save(commit=False) #fills timeline and needs
                project.creator = request.user
                project.title = form_a.cleaned_data['title']
                project.description = form_a.cleaned_data['description']

                if formset.is_valid():
                    project.save() # save project instance
                    for position in formset:
                        position = position.save(commit=False)
                        position.project = project
                        position.save()
                    messages.success(request, 'New project created!')
                    return HttpResponseRedirect(reverse('teams:my_projects'))
    except ValueError:
        messages.error(request, 'Check the form data!')
    return render(request, 'create_project.html', {
        'form_a': form_a, 'form_b': form_b, 'formset': formset,}
    )


# ---- Applications logic ----
def applications(request):
    if request.method == 'GET':
        #applications = request.applications
        #positions = request.positions
        applications = models.Project.objects.all()
    return render(
        request, 'applications.html', {'applications': applications}
    )
