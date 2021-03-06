from django.urls import path

from .customauth_views import (SignUp, LoginAPIView, CurrentUserProfileAPIView, ListUserProfile)

from .posts_views import (InstituteListAPIView, BranchListAPIView, CourseCreateListAPIView,
                            PostCreateListAPIView, PostDetailAPIView, UpVoteAPIView, UserUpVotedPosts,
                            EmailNotificationSubsAPIView, EmailNotiSubsDetailView)

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('login', LoginAPIView.as_view()),
    path('current-user-profile', CurrentUserProfileAPIView.as_view()),
    path('user-profiles', ListUserProfile.as_view()),

    path('institutes', InstituteListAPIView.as_view()),
    path('branches', BranchListAPIView.as_view()),
    path('courses', CourseCreateListAPIView.as_view()),
    path('posts', PostCreateListAPIView.as_view()),
    path('posts/<int:pk>', PostDetailAPIView.as_view()),
    path('upvote', UpVoteAPIView.as_view()),
    path('user-upvoted-posts', UserUpVotedPosts.as_view()),
    path('email-notification-subscription', EmailNotificationSubsAPIView.as_view()),
    path('email-notification-subscription/<int:pk>', EmailNotiSubsDetailView.as_view()),
]