from django.urls import path

from .customauth_views import (SignUp, LoginAPIView, UserProfileAPIView)

from .posts_views import (InstituteListAPIView, BranchListAPIView, CourseCreateListAPIView,
                            PostCreateListAPIView, PostDetailAPIView, UpVoteAPIView, UserUpVotedPosts)

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user-profile', UserProfileAPIView.as_view()),

    path('institutes', InstituteListAPIView.as_view()),
    path('branches', BranchListAPIView.as_view()),
    path('courses', CourseCreateListAPIView.as_view()),
    path('posts', PostCreateListAPIView.as_view()),
    path('posts/<int:pk>', PostDetailAPIView.as_view()),
    path('upvote', UpVoteAPIView.as_view()),
    path('user-upvoted-posts', UserUpVotedPosts.as_view()),
]