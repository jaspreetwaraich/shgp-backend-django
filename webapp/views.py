import uuid

from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.reverse import reverse
from rest_framework import status

from webapp.azure_auth import build_auth_url


def index(request):
    if not request.session.get("user"):
        # TODO: redirect to static page, need FE url
        return JsonResponse({"TODO": "update and redirect to static page"}, status=status.HTTP_200_OK)

    # TODO: update response data requested by FE if needed
    return JsonResponse(request.session.get("user"), status=status.HTTP_200_OK)


def login(request):
    request.session["state"] = str(uuid.uuid4())
    print(request.session["state"])
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    login_url = build_auth_url(request, scopes=settings.SCOPE, state=request.session["state"])
    return redirect(request.build_absolute_uri(login_url))


def logout(request):
    request.session.flush()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        settings.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + request.build_absolute_uri(reverse('authorized')))

