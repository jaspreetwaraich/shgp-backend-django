import requests
import json
from datetime import datetime

from rest_framework import viewsets
from rest_framework.views import Response, status
from rest_framework.decorators import api_view

from django.conf import settings
from django.shortcuts import redirect

from webapp.user_management.models import UserProfile
from webapp.user_management.serializers import UserProfileSerializer
from webapp.azure_auth import get_token_from_cache


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    http_method_names = ['get', 'post', 'update']

    # def retrieve(request, uuid=None): #NOTE: later for update a user info
    # def update(request, uuid=None): #NOTE: later for update a user info

    def create(self, request):
        # Create a new user through the app
        token = get_token_from_cache(request, settings.SCOPE)
        
        if not token:
            return redirect("login")
        
        username = request.data.get("username")
        display_name = request.data.get("name")
        email = request.data.get("email")
        organization = request.data.get("organization")
        job_title = request.data.get("job_title")
        creator = request.data.get("creator") #TODO: get creator
        print ('data.get:', organization)
        
        # POST to Graph API to add a new user to the AD
        user_principalname = username + settings.ORG_DOMAIN
        data = {
                "accountEnabled": "true",
                "displayName": display_name,
                "userPrincipalName": user_principalname,
                "mailNickname": username,
                "passwordProfile" : {
                    "forceChangePasswordNextSignIn": "true",
                    "password": "Shgpnewuser360" #TODO: generate password
                }
            }
        
        response = requests.post(
            '{url}/users'.format(url=settings.GRAPH_API),
            headers={
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + token['access_token']},
            data=json.dumps(data)
            )
        content = json.loads(response.content)

        if response.status_code != 201:
            return Response(
                {
                    'error':'Failed to add the use to Azure AD',
                    'message':content['error']['message']
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        print("post to AAD:", response.content)
        
        # Add new user to the app DB
        uuid = content['id']

        UserProfile.objects.create(
            uuid=uuid,
            username=user_principalname,
            display_name=display_name,
            email=email,
            organization=organization,
            job_title=job_title,
            creator=creator
        )
        return Response({'message':'New user has been created'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_me(request):
    # GET login user info
    token = get_token_from_cache(request, settings.SCOPE)
    
    if not token:
        return redirect('login')
    
    user_info = requests.get(  # Use token to call Graph API
        '{url}/me'.format(url=settings.GRAPH_API),
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return Response(user_info, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_ad_roles(request):
    token = get_token_from_cache(request, settings.SCOPE)
    
    if not token:
        return redirect('login')
    
    response = requests.post(  # Use token to call downstream service
        '{url}/me/getMemberObjects'.format(url=settings.GRAPH_API),
        headers={
            'Content-Type':'application/json',
            'Authorization': 'Bearer ' + token['access_token']},
        data=json.dumps({"securityEnabledOnly": True})
        )
    
    try:
        response.raise_for_status()
        content = response.json()
    except:
        return False
    
    return Response(content['value'], status=status.HTTP_200_OK)

