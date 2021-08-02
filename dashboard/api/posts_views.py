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

from .posts_serializers import (InstituteSerializer, BranchSerializer, CourseSerializer, PostSerializer)
from posts.models import (Institute, Branch, Course,Post, UpVote)
from customauth.models import (User)

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
            return Response({"detail": "User not authorised to perform this operation"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CourseSerializer(data=request.data,partial=True)

        if serializer.is_valid():
            data=serializer.validated_data
            data['created_by']=user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class PostCreateListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer

    def get(self,request,format=None):
        course = self.request.query_params.get('course', None)
        if course is None:
            return Response({"detail": "Please add course id to the query params"}, status=status.HTTP_400_BAD_REQUEST)
        posts = Post.objects.filter(course=course)

        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,format=None):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            user=User.objects.get(id=self.request.user.id)
            data=serializer.validated_data
            data['created_by']=user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)