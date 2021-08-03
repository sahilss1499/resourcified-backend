from django.contrib import admin
from .models import Institute, Branch, Course, Post, UpVote ,EmailNotificationSubscription
# Register your models here.
admin.site.register(Institute)
admin.site.register(Branch)
admin.site.register(Course)
admin.site.register(Post)
admin.site.register(UpVote)
admin.site.register(EmailNotificationSubscription)