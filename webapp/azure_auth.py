import uuid
import requests
import msal

from django.conf import settings
from django.shortcuts import render, redirect
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status


def authorized(request):
    if request.GET.get('state') != request.session.get("state"):
        return redirect("index")  # No-OP. Goes back to Index page
    if "error" in request.GET:  # Authentication/Authorization failure
        return render(request, "auth_error.html", {'result':request.GET})
    if request.GET.get('code'):
        cache = _load_cache(request)
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.GET['code'],
            scopes=settings.SCOPE,  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=request.build_absolute_uri(reverse('authorized')))
        if "error" in result:
            return render(request, "auth_error.html", {'result':result})
        request.session["user"] = result.get("id_token_claims")
        _save_cache(request, cache)
    return redirect("index")


def _load_cache(request):
    cache = msal.SerializableTokenCache()
    if request.session.get("token_cache"):
        cache.deserialize(request.session["token_cache"])
    return cache


def _save_cache(request, cache):
    if cache.has_state_changed:
        request.session["token_cache"] = cache.serialize()


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        settings.CLIENT_ID, authority=authority or settings.AUTHORITY,
        client_credential=settings.CLIENT_SECRET, token_cache=cache)


def build_auth_url(request, authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=request.build_absolute_uri(reverse('authorized')))


def get_token_from_cache(request,scope=None):
    cache = _load_cache(request)  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(request, cache)
        return result