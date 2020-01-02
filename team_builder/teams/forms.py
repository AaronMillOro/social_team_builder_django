from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from . import models


class ProfileForm(forms.ModelForm):
    """Form to populate User basic data"""

    class Meta:
        model = models.Profile
        fields = (
            'fullname', 'bio', 'avatar',
        )
        labels = {
            'fullname': 'ENTER NAME',
            'bio': 'SHORT BIOGRAPHY',
            'avatar': 'UPLOAD PROFILE PICTURE',
        }

    def clean_bio(self):
        '''Validation that biography has 10 or more characters'''
        bio = self.cleaned_data['bio']
        if len(bio) < 10:
            raise forms.ValidationError(
                'BIOGRAPHY MUST HAVE AT LEAST 10 CHARACTERS')
        return bio


class SkillsForm(forms.ModelForm):
    """ User can select the skills provided from database"""
    skills = forms.ModelMultipleChoiceField(
        queryset=models.Skill.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple, label='',
    )

    class Meta:
        model = models.Profile
        fields = ('skills',)


class NewSkillForm(forms.ModelForm):
    """User can add a new skill that is not present in the DB"""
    skill_name = forms.CharField(max_length=20, label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Another skill not cited on the list?'}
        )
    )

    class Meta:
        model = models.Skill
        fields = ('skill_name',)


class ProjectFormPartA(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Project Title'}), label=''
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'Project description'}), label=''
    )

    class Meta:
        model = models.Project
        fields = ('title', 'description',)


class ProjectFormPartB(forms.ModelForm):
    timeline = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Time estimated'}), label='Project Timeline'
    )

    class Meta:
        model = models.Project
        fields = ('timeline', 'requirements',)
        labels = {'requirements': 'Applicant Requirements',}
