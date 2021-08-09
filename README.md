# resourcified-backend
Resouicified is a platform to share and find your valuable resources. This is the public repository of backend of the project. You can view the live website: [https://resourcified.herokuapp.com/](https://resourcified.herokuapp.com/). Backend is live at: [ https://api-resourcified.herokuapp.com/]( https://api-resourcified.herokuapp.com/)     
**Frontend Public Repository-** [https://github.com/ParthKhanna07/resourcified-frontend-public](https://github.com/ParthKhanna07/resourcified-frontend-public)

**Tech Stack-** Django, Django Rest Framework, PostgreSQL

## Project Setup Guide:
- Clone the repository
- After going into the required directory make a vitual environment and activate it (optional but preferrable)
- Run `pip install -r requirements.txt`  to install all the requirements/dependencies. 
(**Note**- Your system must have python installed (version >= 3.7.6))
- You will have to run a migration to make the specific tables in the database so run the following command terminal:      
 `python manage.py migrate`        
- **Creating superuser**- This will give you the access to the admin page of the website. To make a superuser run `python manage.py createsuperuser` in the terminal and specify the details.
- Now you are good to go! Finally run `python manage.py runserver` or `python manage.py runserver <hostip>`to run the django application.

