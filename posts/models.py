from django.db import models
from customauth.models import User
# Create your models here.

class Institute(models.Model):
    name = models.CharField(max_length=250)
    email=models.EmailField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by = models.ForeignKey(User, related_name='institute_created_by', on_delete=models.PROTECT,blank=True,null=True)
    modified_by = models.ForeignKey(User, related_name='institute_modified_by', on_delete=models.PROTECT,blank=True,null=True)
    
    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=250)
    institute = models.ForeignKey(Institute, related_name="institute_branch", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by = models.ForeignKey(User, related_name='branch_created_by', on_delete=models.PROTECT,blank=True,null=True)
    modified_by = models.ForeignKey(User, related_name='branch_modified_by', on_delete=models.PROTECT,blank=True,null=True)

    def __str__(self):
        return f"{self.name} {self.institute}"


class Course(models.Model):
    name = models.CharField(max_length=250)
    branch = models.ForeignKey(Branch, related_name="branch_course", on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, related_name="institute_course", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by = models.ForeignKey(User, related_name='course_created_by', on_delete=models.PROTECT,blank=True,null=True)
    modified_by = models.ForeignKey(User, related_name='course_modified_by', on_delete=models.PROTECT,blank=True,null=True)

    def __str__(self):
        return f"Name:{self.name},Branch:{self.branch},Insti:{self.institute}"


class Post(models.Model):
    link = models.URLField()
    description = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Course, related_name="post_for_course", on_delete=models.CASCADE)
    upvote_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by = models.ForeignKey(User, related_name='post_created_by', on_delete=models.PROTECT,blank=True,null=True)
    modified_by = models.ForeignKey(User, related_name='post_modified_by', on_delete=models.PROTECT,blank=True,null=True)

    def __str__(self):
        return f"User: {str(self.created_by.email)} PostID: {self.id}"


class UpVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="upvote_by")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="upvote_for_post")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        unique_together = ('user','post')

    def __str__(self):
        return f"User: {self.user.email}, Post: {self.post}"