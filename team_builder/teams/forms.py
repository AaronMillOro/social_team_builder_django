from django import forms

from . import models


class ProfileForm(forms.ModelForm):
    """Form to populate User basic data"""

    class Meta:
        model = models.Profile
        fields = (
            'fullname', 'bio', 'avatar',
        )
        required = ('fullname',)
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
    skill_name = forms.CharField(
        max_length=20, label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Another skill not cited on the list?', }
        )
    )

    class Meta:
        model = models.Skill
        fields = ('skill_name',)


class ProjectFormPartA(forms.ModelForm):
    """ User can create a new project Part A """
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Project Title'}), label='')
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Project description'}), label='')

    class Meta:
        model = models.Project
        fields = ('title', 'description',)


class ProjectFormPartB(forms.ModelForm):
    """ User can create a new project Part B """
    timeline = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Time estimated'}), label='Project Timeline')

    class Meta:
        model = models.Project
        fields = ('timeline', 'requirements',)
        labels = {'requirements': 'Applicant Requirements', }


class PositionForm(forms.ModelForm):
    """ User can add required Positions to a Project """
    related_skill = forms.ModelChoiceField(
        queryset=models.Skill.objects.all(),
        widget=forms.Select(attrs={'class': 'related_skill'}), )

    class Meta:
        model = models.Position
        fields = ('name', 'description', 'related_skill',)


PositionFormSet = forms.modelformset_factory(
    models.Position, extra=0, min_num=1,
    fields=('name', 'description', 'related_skill')
)


class ApplicationForm(forms.ModelForm):
    """The creator of a Project can select the candidate that applied"""
    status = forms.ChoiceField(choices=[
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
        ], label='',
    )

    class Meta:
        model = models.Application
        fields = ('status',)
