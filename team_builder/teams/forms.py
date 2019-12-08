from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from . import models


class ProfileForm(forms.ModelForm):

    class Meta:
        model = models.Profile
        fields = (
            'fullname', 'bio', 'avatar', 'skills',
        )
        labels = {
            'fullname': 'Provide your entire name',
            'bio': 'Short biography',
            'Skills': 'Provide your dev skills',
        }

    def clean_bio(self):
        ''' Validation that biography has 10 or more characters'''
        bio = self.cleaned_data['bio']
        if len(bio) < 10:
            raise forms.ValidationError(
                'The biography must have at least 10 characters')
        return bio
