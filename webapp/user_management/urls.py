from django.conf.urls import re_path, include
from rest_framework.routers import DefaultRouter
from webapp.user_management.endpoints import get_me, get_ad_roles, UserProfileViewSet


router = DefaultRouter()

router.register(
    r'api/v1/users',
    UserProfileViewSet,
    basename='user_profile'
) # FE: POST json in body to create new user
'''
POST body example:
{
    "username": "test_2",
    "name": "Test Two",
    "email": "test2@test.ca",
    "organization": "",
    "job_title": "Researcher",
    "creator" : "user admin test" #Can FE send log-in user's username? 
}
'''

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^api/v1/me', get_me , name='me'),
    re_path(r'^api/v1/myroles', get_ad_roles , name='ad_roles'),
]
