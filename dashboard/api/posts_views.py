from functools import partial
from rest_framework import permissions, status, filters
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django.db.models import Count

from .posts_serializers import (InstituteSerializer, BranchSerializer, CourseSerializer, PostSerialzier, 
                                PostShowSerializer, UpVoteSerializer)
from posts.models import (Institute, Branch, Course,Post, UpVote)
from customauth.models import (User)

  
import logging
logger = logging.getLogger('')

class InstituteListAPIView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = InstituteSerializer

    def get_queryset(self):
        queryset = Institute.objects.all().order_by('-id')
        return queryset



class BranchListAPIView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BranchSerializer

    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['institute']

    def get_queryset(self):
        queryset = Branch.objects.all().order_by('-id')
        return queryset


class CourseCreateListAPIView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CourseSerializer

    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['branch','institute']

    def get_queryset(self):
        queryset = Course.objects.all().order_by('-id')
        return queryset

    def post(self,request,format=None):
        user=User.objects.get(id=self.request.user.id)

        if user.role != 'admin':
            logger.warning(f"unauthorized attempt to POST a new course by {user.email}")
            return Response({"detail": "User not authorised to perform this operation"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CourseSerializer(data=request.data,partial=True)

        if serializer.is_valid():
            data=serializer.validated_data
            data['created_by']=user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class PostCreateListAPIView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostShowSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['course','created_by']

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-created_at')
        return queryset

    def post(self,request,format=None):
        serializer = PostSerialzier(data=request.data,context={'request':request})

        if serializer.is_valid():
            user=User.objects.get(id=self.request.user.id)
            data=serializer.validated_data
            data['created_by']=user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)




class PostDetailAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostShowSerializer

    def get_object(self,pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        post = self.get_object(pk)
        serializer = PostShowSerializer(post,context={'request':request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,pk,format=None):
        post = self.get_object(pk)
        
        if post.created_by.id != self.request.user.id:
            logger.warning(f"unauthorized attempt to MODIFY a post ({post}) by {self.request.user.email}")
            return Response({"detail": "User not authorised to perform this operation"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = PostSerialzier(post, request.data, context={'request':request},partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        print(post.created_by)
        print(self.request.user.id)
        if post.created_by.id != self.request.user.id:
            logger.warning(f"unauthorized attempt to DELETE a post ({post}) by {self.request.user.email}")
            return Response({"detail": "User not authorised to perform this operation"}, status=status.HTTP_401_UNAUTHORIZED)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UpVoteAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpVoteSerializer

    def post(self,request,format=None):
        serializer = UpVoteSerializer(data=request.data)
        post = Post.objects.get(id=request.data["post"])

        if serializer.is_valid():
            serializer.save()
            post.upvote_count += 1
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            upvote = UpVote.objects.get(post=request.data["post"], user=request.data["user"])
            upvote.delete()
            post.upvote_count -= 1
            post.save()
            return Response({"detail": "UpVote deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




class UserUpVotedPosts(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,format=None):
        upvote_qs = UpVote.objects.filter(user=self.request.user.id)
        post_ids = []

        for upvote in upvote_qs:
            post_ids.append(upvote.post.id)
        
        posts = Post.objects.filter(id__in=post_ids)
        serializer = PostShowSerializer(posts,context={'request':request},many=True)

        return Response(serializer.data)
