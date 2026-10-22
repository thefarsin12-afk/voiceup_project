from rest_framework import serializers

from feedback.models import FeedbackModel 

from django.contrib.auth.models import User

class UserRegistrationSerailizer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ["username","email","password"]

class FeedbackSerailizer(serializers.ModelSerializer):

    department = serializers.CharField(allow_blank=True)

    feedback_text = serializers.CharField(allow_blank=True)

    class Meta:

        model = FeedbackModel

        fields = "__all__"

        read_only_fields = ["id","student","created_at"]

    def validate_department(self,validate_data):

        if not validate_data or not validate_data.strip():

            raise serializers.ValidationError("Department cannot be empty.")

        return validate_data.strip()

    def validate_feedback_text(self,validate_data):

        if not validate_data or not validate_data.strip():

            raise serializers.ValidationError("Feedback text cannot be empty.")

        if len(validate_data.strip()) < 5:

            raise serializers.ValidationError("Feedback must contain at least 10 characters.")

        return validate_data.strip()
    

        