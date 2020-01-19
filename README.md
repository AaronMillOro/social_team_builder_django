# Social team builder with Django

This project was build from scratch using the Python framework [Django](https://www.djangoproject.com/).

This site was build with the aim to help people from a community to work together based on their skills.

In the site, people can sign up to find projects that need help or post their own projects for other people to
join. Users should be able to create a brief profile for themselves after they sign up with an avatar, a bio, and pick their skills from a list, or even add a new skill. 

Users can post a project, too, giving it a title and description. They should also list the positions they need filled for that job with a brief description of what the position will be responsible for. 

Users should be able to find a project and ask to join it. If you're a project owner, you can approve or deny the person asking to join. 


## Project content

* A defined format was supplied as well as static assets that were used for the templates for the web site.
* The user of the site is able to **sign up** for, **log into** and **log out** from an account.
* The user can **edit the profile** space, being able to : 
	* Upload an avatar image for the profile.
	* Add a brief description
	* Pick the skills for the profile, or even add a new skill.
* The user can **create a project** and specify the **positions** that project. Each position has a name, a description, and related skill.
* The user that created a given project can see all of the applicants for that project's positions.
* The user that created a given project can **approve/reject an applicant** for a position.
* A notification is showed to the user revealing if that person was rejected or approved for a position.
* The user can search for projects based on words in their titles or descriptions (use of querysets).
* The user can filter projects by the positions they need filled.
* The user can **apply for a position** in another project.
* Unit test coverage is accesible by typing:
	
		coverage report

![Figure display](https://github.com/AaronMillOro/social_team_builder_django/blob/master/team_builder/media/images/social_team.png)

## Code of commits

| Emoji | code | Description|
---|---|---
| :lollipop: | : lollipop : | Minor change |
| :pencil2: | : pencil2 : | Add of new code |
| :wrench: | : wrench : | Code refactoring | 
| :checkered_flag: | : checkered_flag : | Unit tests | 


## Test the app

1. Install (if required) and run pipenv.

		pipenv install
		
		pipenv shell

2. Download the corresponding dependencies in the virtual environment. 

		pip install -r requirements.txt
		

3. Run the application.
		
		python3 manage.py runserver 0.0.0.0:5000

4. Open your favorite web browser and type:

		http://localhost:5000/

Enjoy! :shipit: