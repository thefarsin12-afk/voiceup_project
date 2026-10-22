from django.urls import path

from feedback.views import UserRegistrationView
from rest_framework.authtoken.views import ObtainAuthToken
from feedback.views import FeedbackListCreateView,FeedbackRetriveUpdateDeleteView
from feedback.views import FeedBackSummariView


urlpatterns = [

    # ==== USER SECTION ====
    # sign in
    path("signup/",UserRegistrationView.as_view()),

    # login - Token Generate
    path('signin/',ObtainAuthToken.as_view()),

    # Feedback List Create View
    path('feedback/',FeedbackListCreateView.as_view()),

    # Feedaback Retrieve Update Delete
    path('feedback/<int:pk>/',FeedbackRetriveUpdateDeleteView.as_view()),

    # Feedback SummaryView
    path('feedback/summary/',FeedBackSummariView.as_view()),

]