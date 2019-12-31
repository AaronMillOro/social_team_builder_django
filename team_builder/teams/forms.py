from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from . import models


class ProfileForm(forms.ModelForm):

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
        ''' Validation that biography has 10 or more characters'''
        bio = self.cleaned_data['bio']
        if len(bio) < 10:
            raise forms.ValidationError(
                'BIOGRAPHY MUST HAVE AT LEAST 10 CHARACTERS')
        return bio


class SkillsForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=models.Skill.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple, label='',
    )
    #skills = forms.MultipleChoiceField(
    #skills = forms.ModelChoiceField(
        #queryset=models.Skill.objects.values_list('skill_name',flat=True).distinct(),
    #    choices=models.Skill.objects.all().values_list(),
    #    widget=forms.CheckboxSelectMultiple,
    #
    #)

    class Meta:
        model = models.Profile
        fields = ('skills',)


class NewSkillForm(forms.ModelForm):
    skill_name = forms.CharField(max_length=20, label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Another skill not cited on the list?'}
        )
    )

    class Meta:
        model = models.Skill
        fields = ('skill_name',)
