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
                'BIOGRAPHY FIELD MUST HAVE AT LEAST 10 CHARACTERS')
        return bio


class SkillsForm(forms.ModelForm):
    skills = forms.MultipleChoiceField(
        choices=SKILLS,
        widget=forms.CheckboxSelectMultiple, 
    )

    class Meta:
        model = models.Profile
        fields = ('skills',)
