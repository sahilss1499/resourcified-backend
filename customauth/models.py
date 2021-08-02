from django.db import models
from django.contrib.auth.models import AbstractUser


import uuid

# Create your models here.
class User(AbstractUser):
    role_choices = (
        ('student','student'),
        ('admin','admin'),
    )
    gender_choices = (
        ('male', 'male'),
        ('female', 'female'),
        ('other','other'),
    )
    degree_choices = (
        ('btech', 'btech'),
        ('mtech', 'mtech'),
        ('phd','phd'),
        ('msc','msc'),
        ('mba','mba'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField(blank=True, null=True)
    full_name = models.CharField(max_length=300)
    role = models.CharField(choices=role_choices,max_length=50,blank=True, null=True)
    branch = models.ForeignKey('posts.Branch', related_name="user_branch", blank=True, null=True, on_delete=models.CASCADE)
    institute = models.ForeignKey('posts.Institute', related_name="user_institute", blank=True, null=True, on_delete=models.CASCADE)

    profile_image = models.FileField(upload_to='profile/',blank=True, null=True)
    gender = models.CharField(
        max_length=50, choices=gender_choices, blank=True, null=True)
    degree = models.CharField(
        max_length=50, choices=degree_choices, blank=True, null=True)
    

    joined_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{str(self.id)} {self.email}"