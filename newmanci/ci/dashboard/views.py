from datetime import date
import json
import urllib2
import datetime
import hashlib
import os
import collections

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from annoying.decorators import render_to
from ci import settings
from os.path import join
from glob import glob


from dashboard.models import User
from dashboard.forms import UserForm

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

"""
Purpose: 404 Not Found View
Input: Form, Function, Class, or Resource
Returns: View
"""
def custom_404(request):
    return render(request, '404.html')

"""
Purpose: 500 Server Error
Input: Form, Function, Class, or Resource
Returns: View
"""
def custom_500(request):
    return render(request, '500.html')

@login_required
# Create your views here.
def index(request):
    context = RequestContext(request)
    file_contents_dict = collections.OrderedDict()
    json_content_dict = collections.OrderedDict()
    master_dict = collections.OrderedDict()
    for key, value in settings.NEWMANCI_SOURCE_LIST.iteritems():
        counter = settings.NEWMANCI_COUNTER_START
        for f in glob(join(join(settings.NEWMANCI_LOG_DIR, key), '*.txt')):
            if counter <= settings.NEWMANCI_MAX_DASHBOARD_COUNTER:
                file_contents_dict[key+'_txt_'+str(counter)] = {f: open(f, 'rb').read()}
            counter += 1
        counter = settings.NEWMANCI_COUNTER_START
        for j in glob(join(join(settings.NEWMANCI_LOG_DIR, key), '*.json')):
            if counter <= settings.NEWMANCI_MAX_DASHBOARD_COUNTER:
                json_content_dict[key+'_json_'+str(counter)] = {f: open(j, 'rb').read()}
            counter += 1
        master_dict['file'] = file_contents_dict
        master_dict['json'] = json_content_dict
    return render_to_response('index.html', {'master_dict': master_dict}, context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    #print context
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can logs the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't logs the user in.
            #print "Invalid login details: {0}, {1}".format(username, password)
            return render(request, 'login.html', {'bad_details': 'True'})
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)

@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render_to_response(
        'register.html',
        {'user_form': user_form,
         'registered': registered},
        context
        )