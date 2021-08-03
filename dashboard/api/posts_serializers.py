from rest_framework import serializers

from posts.models import Institute, Branch, Course, Post, UpVote

from .customauth_serializers import UserProfileSerializer

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

class PostSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')

class PostShowSerializer(serializers.ModelSerializer):
    is_already_upvoted = serializers.SerializerMethodField(read_only=True)
    created_by = UserProfileSerializer()
    class Meta:
        model = Post
        # fields = ('link','description','course','upvote_count','created_at','modified_at','created_by','modified_by','already_upvoted')
        fields = ('__all__')

        extra_kwargs = {
            'upvote_count':{'read_only':True},
            }
        
    def get_is_already_upvoted(self,obj):
        try:
            # checking if the current user who sent the request has upvoted this particular post
            upvote = UpVote.objects.get(user=self.context['request'].user.id, post=obj.id)
            return True
        except UpVote.DoesNotExist:
            return False



class UpVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpVote
        fields = ('__all__')