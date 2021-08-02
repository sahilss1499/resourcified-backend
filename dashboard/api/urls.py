from django.urls import path

from .customauth_views import (SignUp, LoginAPIView,)

from .posts_views import (InstituteListAPIView, BranchListAPIView, CourseCreateListAPIView,
                            PostCreateListAPIView,)

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('login', LoginAPIView.as_view()),

    path('institutes', InstituteListAPIView.as_view()),
    path('branches', BranchListAPIView.as_view()),
    path('courses', CourseCreateListAPIView.as_view()),
    path('posts', PostCreateListAPIView.as_view()),
]