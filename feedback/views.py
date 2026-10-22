from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from feedback.models import FeedbackModel
from feedback.serializer import UserRegistrationSerailizer
from feedback.serializer import FeedbackSerailizer
from feedback.permission import IsOwner
from feedback.ai_integration import sentiment_and_category

class UserRegistrationView(APIView):

    def post(self,request):

        form_data = request.data

        serializer = UserRegistrationSerailizer(data=form_data)

        if serializer.is_valid():

            cleaned_data = serializer.validated_data

            qs = User.objects.create_user(**cleaned_data)

            serializer = UserRegistrationSerailizer(qs)

            return Response(data=serializer.data)

        else:
            return Response(data=serializer.errors)        

class FeedbackListCreateView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        qs = FeedbackModel.objects.all()

        seraializer = FeedbackSerailizer(qs,many=True)

        return Response(data=seraializer.data)

    def post(self,request):

        auth_user = request.user

        form_data = request.data

        serialize = FeedbackSerailizer(data=form_data)

        if serialize.is_valid():

            classification = sentiment_and_category(
                serialize.validated_data["feedback_text"]
            )
            serialize.save(student=auth_user, **classification)

            return Response(data=serialize.data)

        else:
            return Response(data=serialize.errors)


class FeedbackRetriveUpdateDeleteView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [IsOwner]

    def get(self,request,pk=None):

        instance = get_object_or_404(FeedbackModel,id=pk)

        self.check_object_permissions(request,instance)

        serializer = FeedbackSerailizer(instance)

        return Response(data=serializer.data)

    def put(self,request,pk=None):

        instance = get_object_or_404(FeedbackModel,id=pk)

        self.check_object_permissions(request,instance)

        form_data = request.data

        serializer = FeedbackSerailizer(data=form_data,instance=instance)

        if serializer.is_valid():

            serializer.save()

            return Response(data=serializer.data)

        else:
            return Response(data=serializer.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(FeedbackModel,id=pk)

        instance.delete()

        response_data = {"message":"deleted"}

        return Response(data=response_data)        

class FeedBackSummariView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

      response_data = {

          "sentiment_summary":0,
          "category_summary":0,
      }

      summari_wise = FeedbackModel.objects.filter(student=request.user)

      if summari_wise:

        sentiment_summary = summari_wise.values("sentiment").annotate(sentiment_summary=Count("id"))

        category_summary = summari_wise.values("category").annotate(category_summary=Count("id"))

        response_data ["sentiment_summary"] = sentiment_summary

        response_data ["category_summary"] = category_summary

        return Response(data=response_data)





            

        



