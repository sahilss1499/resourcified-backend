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

from resourcified.settings import FRONTEND_BASE_URL

from .posts_serializers import (InstituteSerializer, BranchSerializer, CourseShowSerializer, CourseSerializer, PostSerialzier, 
                                PostShowSerializer, UpVoteSerializer, EmailNotificationSubsSerializer)
from posts.models import (Institute, Branch, Course,Post, UpVote, EmailNotificationSubscription)
from customauth.models import (User)

from .email_service import sendMail, sendHTMLPostMail
  
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
    serializer_class = CourseShowSerializer

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
        
        serializer = CourseSerializer(data=request.data,context={'request':request},partial=True)

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
            course_name = data['course'].name
            data['created_by']=user
            serializer.save()
            # to send email notification to the users who have subscribed to the course where the post is created
            subscribed_user_emails = []
            email_noti_subs_qs = EmailNotificationSubscription.objects.filter(course=serializer.data["course"])
            for obj in email_noti_subs_qs:
                subscribed_user_emails.append(obj.user.email)
            
            subject=f"{user.full_name} just added a new resource for the course {course_name} do check it out!"
            post_id = serializer.data["id"]
            frontend_url = f"{FRONTEND_BASE_URL}posts/{post_id}"
            message = f"Check out the post @ {frontend_url}"
            # sendMail(subject=subject, message=message, recipient_list=subscribed_user_emails)
            sendHTMLPostMail(subject=subject,
                            post_created_by=user.full_name,
                            course_name=course_name,
                            frontend_url=frontend_url,
                            recipient_list=subscribed_user_emails)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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
            user=User.objects.get(id=self.request.user.id)
            data=serializer.validated_data
            data['modified_by']=user
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


# create and list email notifiction list
class EmailNotificationSubsAPIView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EmailNotificationSubsSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['user']

    def get_queryset(self):
        queryset = EmailNotificationSubscription.objects.all().order_by('-created_at')
        return queryset

    def post(self,request,format=None):
        serializer = EmailNotificationSubsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "you are already subscribed"}, status=status.HTTP_400_BAD_REQUEST)




class EmailNotiSubsDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EmailNotificationSubsSerializer

    def get_object(self,pk):
        try:
            return EmailNotificationSubscription.objects.get(pk=pk)
        except EmailNotificationSubscription.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        email_noti_obj = self.get_object(pk)
        serializer = EmailNotificationSubsSerializer(email_noti_obj)
        return Response(serializer.data)
    
    def delete(self, request, pk, format=None):
        email_noti_obj = self.get_object(pk)
        logger.info(f"{email_noti_obj.user} Subscription deleted for {email_noti_obj.course}")
        email_noti_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)