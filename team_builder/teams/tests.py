from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.test import Client, TestCase
from django.urls import reverse

from .forms import (ApplicationForm, NewSkillForm, PositionFormSet,
                    ProjectFormPartA, ProjectFormPartB, ProfileForm,
                    SkillsForm)
from .models import (Application, Position, Project, Profile, Skill,
                     create_user_profile)
from . import views


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(
            username='David', password='nitaLA2019'
        )
        self.client.login(username='David', password='nitaLA2019')
        skill_1 = Skill.objects.create(skill_name='CSS')
        skill_2 = Skill.objects.create(skill_name='Python')

        @receiver(post_save, sender=user)
        def create_user_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.create(user=instance)

    def test_add_skill(self):
        skills = Skill.objects.all()
        response = self.client.get(reverse('teams:add_skills'))
        form = SkillsForm(data={'skill_name': 'GOlang'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.is_valid())
        self.assertTemplateUsed(response, 'add_skills.html', 'layout.html')
        self.assertEqual(2, len(skills))

    def test_create_profile_form(self):
        data = {'fullname': 'David Moyes', 'bio': 'bla bla bla',
            'avatar': 'image.png'
        }
        form = ProfileForm(data=data)
        response = self.client.post(reverse('teams:profile_edit'), data)
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        # set profile data to display on view
        profile = Profile.objects.last()
        profile.fullname = 'David Moyes'
        profile.bio = 'bla bla bla'
        profile.avatar = 'image.png'
        profile.save()
        response = self.client.get(reverse('teams:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html', 'layout.html')
        self.assertEqual(profile.fullname, 'David Moyes')

    def test_project_create(self):
        profile = Profile.objects.last()
        data_a = {'title': 'New project', 'description': 'Project descript'}
        form_a = ProjectFormPartA(data=data_a)
        data_b = {
            'timeline': 'Approximate timming',
            'requirements': 'Requirements of project',
        }
        form_b = ProjectFormPartB(data=data_b)
        skill_1 = Skill.objects.create(skill_name='CSS')
        response = self.client.get(reverse('teams:create_project'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project_create.html', 'layout.html')
        self.assertTrue(form_a.is_valid())
        self.assertTrue(form_b.is_valid())
