from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from . import models

SKILLS = [
    ('HTML/CSS', 'HTML/CSS'),
    ('Wordpress', 'Wordpress'),
    ('JavaScript', 'JavaScript'),
    ('Ruby', 'Ruby'),
    ('Django', 'Django'),
    ('GOlang', 'GOlang'),
    ('Android', 'Android'),
    ('R', 'R'),
    ('Python', 'Python'),
]


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
    skills = forms.MultipleChoiceField(
        choices=models.Skill.objects.all().values_list(),
        #choices=SKILLS,
        widget=forms.CheckboxSelectMultiple,
        label=''
    )

    class Meta:
        model = models.ProfileSkills
        fields = ('skills',)


class NewSkillForm(forms.ModelForm):
    skill_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Other skill ?'}),
        label='',
    )

    class Meta:
        model = models.Skill
        fields = ('skill_name',)
