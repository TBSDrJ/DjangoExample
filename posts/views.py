### Python version 3.7.4
### Django version 3.0.3

from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
# Add my models and my forms
from .models import Post, Following, Profile
from .forms import PostForm
# These are needed for user authentication and persistence
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

class IndexView(View):
    # All posts will appear in all versions of the IndexView, so make it
    #   available to the entire class.
    allPosts = Post.objects.order_by("-pubDate")

    def get(self, request):
        # We'll use the built-in authenticaion form
        form = AuthenticationForm()
        # Send the template the form and the posts.
        context = {
            'form': form,
            'allPosts': self.allPosts,
            'user': request.user,
        }
        return render(request, 'posts/index.html', context)

    def post(self, request):
        # First check if we are coming here after hitting 'Logout'
        if 'logout' in request.POST.keys():
            # Then log out
            logout(request)
            # We load an empty form with no data
            form = AuthenticationForm()
        else:
            # We're if we got her after hitting 'Login'
            # So we match up the data with the form fields
            form = AuthenticationForm(data=request.POST)
            # Validate and clean the data
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                # Then authenticate and log in.
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user = user)
        # Set up the data for the template
        context = {
            'form': form,
            'allPosts': self.allPosts,
        }
        # And send to template
        return render(request, 'posts/index.html', context)

class UsernameView(View):
    def get(self, request, username):
        # Need to track down the User object before getting Posts
        thisUser = User.objects.get(username = username)
        # I've layered on both a filter and a sort on this query
        thisUsersPosts = Post.objects.filter(
            userPosted = thisUser).order_by('-pubDate')
        if request.user.username == username:
            # If we're here, the user is on their own page.
            form = PostForm()
            context = {
                'form': form,
                'thisUser': request.user,
                'thisUsersPosts': thisUsersPosts,
            }
            return render(request, 'posts/usernamepage.html', context)
        else:
            if request.user.is_authenticated:
                # If we're here, we have an authenticated user but
                # not at their own home page
                print('Authenticated user, not home')
            else:
                # If we're here, we have non-authenticated user
                print('Not an authenticated user.')
        return HttpResponse('UsernameView Get')
    def post(self, request, username):
        return HttpResponse('UsernameView Post')

class FollowedView(View):
    def get(self, request, username):
        return HttpResponse('FollowedView Get')
    def post(self, request, username):
        return HttpResponse('FollowedViewPost')
