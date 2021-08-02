from rest_framework import serializers

from posts.models import Institute, Branch, Course, Post

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ('__all__')

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('__all__')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('__all__')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')

        extra_kwargs = {
            'upvote_count':{'read_only':True},
            }