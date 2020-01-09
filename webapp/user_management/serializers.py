from rest_framework import serializers
from webapp.user_management.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('oid', 'username', 'display_name', 'email', 'organization', 'job_title', 'creator', 'created')
