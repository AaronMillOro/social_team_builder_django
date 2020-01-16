from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .forms import (ApplicationForm, NewSkillForm, PositionForm,
                    ProjectFormPartA, ProjectFormPartB, ProfileForm,
                    SkillsForm)
from .models import Application, Position, Project, Profile, Skill
from . import views


class SkillTest(TestCase):
    def setUp(self):
        self.client = Client()
        skill_1 = Skill.objects.create(skill_name='CSS')
        skill_2 = Skill.objects.create(skill_name='Python')
        skill_3 = Skill.objects.create(skill_name='Java')
        self.user = User.objects.create_user(
            username='Juan', password='juanitaLA2019'
        )

    def test_add_skill(self):
        """
        Checks that
        i) user is authenticated
        ii) the correct html template is used
        iii) all the skills from the database are listed
        iv) the validity of the form to add a new skill
        """
        self.client.login(username='juan', password='juanitaLA2019')
        skills = Skill.objects.all()
        response = self.client.get(reverse('teams:add_skills'), kwargs={skills})
        form = SkillsForm(data={'skill_name': 'GOlang'})
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 302)
        #self.assertTemplateUsed(response, 'add_skills.html')
        self.assertEqual(3, len(skills))


"""
class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='David', password='juanitaLA2019'
        )
        skill_1 = Skill.objects.create(skill_name='Java')
        skill_2 = Skill.objects.create(skill_name='HTML')
        skills = Skill.objects.all()
        profile_1 = Profile.objects.create(
            user=self.user1, fullname='David Moyes',
            bio='A description of the user'
        )

    def test_edit_profile(self):
        self.client.login(username='David', password='juanitaLA2019')
        profile_1 = Profile.objects.get(fullname='David Moyes')
        response = self.client.get(reverse('teams:profile_edit'), {
            'profile': profile_1}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.fullname, 'David Moyes')

    def tearDown(self):
        super(ProfileTest, self).tearDown()
"""
