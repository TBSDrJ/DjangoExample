### Python version 3.7.4
### Django version 3.0.3

from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
# Add my models
from .models import Post, Following, Profile
# These are needed for user authentication and persistence
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

class IndexView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, 'posts/index.html', context)
    def post(self, request):
        return HttpResponse('IndexView Post')

class UsernameView(View):
    def get(self, request, username):
        return HttpResponse('UsernameView Get')
    def post(self, request, username):
        return HttpResponse('UsernameView Post')

class FollowedView(View):
    def get(self, request, username):
        return HttpResponse('FollowedView Get')
    def post(self, request, username):
        return HttpResponse('FollowedViewPost')
