
### Python version 3.7.4
### Django version 3.0.3

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Custom imports added
# Add my model
from .models import Post, Following
# Need timezone for date/time published
from django.utils import timezone
# These are needed for user authentication and persistence
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# This is a Pretty Print module that makes it easier to read when you dump
#  the entire contents of a large dictionary to screen.
import pprint

# This is the home view if you just type in a basic URL with nothing added
def index(request):
    # It has forms that redirect to itself, so check if this form data is present
    if request.POST:
        # This tests if the form is the log *in* form
        if 'inputUsername' in request.POST.keys():
            # IF so, try to authentircate
            user = authenticate(username=request.POST['inputUsername'],
                password=request.POST['inputPassword'])
            if user is not None:
                # IF success, then use the login function so the session persists.
                login(request, user)
            else:
                pass
                # Message for failed login.
        # This tests if the form is the log *out* form
        elif 'logout' in request.POST.keys():
            # If so, don't need to check anything else, just kill the session.
            logout(request)
    # After we check the forms, set a flag for use in the template.
    loggedIn = request.user.is_authenticated
    # Find the template
    template = loader.get_template('posts/index.html')
    # The home page will show *all* posts for now.
    allPosts = Post.objects.order_by('-pubDate')
    # The Post model only contains the username, so we go and fetch the
    # first and last names from the User model and add that information.
    for post in allPosts:
        poster = post.userPosted
        post.firstName = poster.first_name
        post.lastName = poster.last_name
    # Now all the data is ready to pass to the template so set up the context.
    context = {
        'allPosts': allPosts,
        'loggedIn': loggedIn,
        'user': request.user,
        }
    # And go!
    return HttpResponse(template.render(context, request))

def followed(request, username):
    # Make sure that this user exists before we get the user info.
    # Show error page if user does not exist.
    try:
        thisUser = User.objects.get(username=username)
    except:
        template = loader.get_template('posts/nosuchusername.html')
        context = {
            'username': username,
            }
        return HttpResponse(template.render(context, request))
    template = loader.get_template('posts/followed.html')
    # Check if anyone is logged in
    if request.user.is_authenticated:
        # If logged in, check if that user is looking at their own page
        if request.user.username == username:
            # Get list of people who this user follows
            follows = Following.objects.filter(follower = thisUser)
            # Get their posts
            followedPosts = []
            for follow in follows:
                followed = User.objects.get(username = follow.followed)
                followedPosts += Post.objects.filter(userPosted = followed)
            # Put them in order by date posted
            followedPosts = sorted(followedPosts,
                key=lambda post: post.pubDate)
            followedPosts.reverse()
            context = {
                'thisUser': thisUser,
                'followedPosts': followedPosts,
                'loggedIn': True,
                'isPageOwner': True,
            }
    return HttpResponse(template.render(context, request))

def usernamepage(request, username):
    # Use the Pretty Printer to make this giant mess vaguely readable.
    # Notice that the vars() function means I see *all* of the dictionary
    #   instead of just the __str()__ method version of it.
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(vars(request))

    # Make sure that this user exists before we get the user info.
    # Show error page if user does not exist.
    try:
        userInfo = User.objects.get(username=username)
    except:
        template = loader.get_template('posts/nosuchusername.html')
        context = {
            'username': username,
            }
        return HttpResponse(template.render(context, request))
    if request.user.is_authenticated:
        # Check if the authenticated user is looking at their own page.
        if request.user.username == username:
            # This page has a form to add a post that redirects to itself, so
            #   check if that form was filled out or not.
            if request.POST:
                # Create an instance of the Post object.
                newPost = Post(
                    postText = request.POST['newPostText'],
                    userPosted = request.POST['userPosting'],
                    pubDate = timezone.now(),
                    )
                # Save to the database.
                newPost.save()
            # Get all the posts for this user only *after* we've added the new one if that happened.
            myPosts = Post.objects.filter(userPosted = userInfo.id)
            # Now, cut this down to the most recent and put in order
            latestPosts = myPosts.order_by('-pubDate')[:5]
            # Go find the template
            template = loader.get_template('posts/usernamepage.html')

            # Load up the data into a context.
            context = {
                'latestPosts': latestPosts,
                'userInfo': userInfo,
                'isPageOwner': True,
                'loggedIn': True
                }
            # And go!
            return HttpResponse(template.render(context, request))
        else:
            # Authenticated, but looking at someone else's page

            # Get all of this user's posts (user whose page we're on)
            userPosts = Post.objects.filter(userPosted = userInfo.id)
            # Now, cut this down to the most recent and put in order
            latestPosts = userPosts.order_by('-pubDate')[:5]
            # Go find the template
            template = loader.get_template('posts/usernamepage.html')
            # Load up the data into a context.
            context = {
                'latestPosts': latestPosts,
                'userInfo': userInfo, # whose page we're on
                'isPageOwner': False,
                'loggedIn': True,
                'whoIsIt': request.user.username, # who is logged in
                }
            # And go!
            return HttpResponse(template.render(context, request))
    else:
        # Not authenticated at all.

        # Get all of this user's posts
        userPosts = Post.objects.filter(userPosted = userInfo.id)
        # Now, cut this down to the most recent and put in order
        latestPosts = userPosts.order_by('-pubDate')[:5]
        # Go find the template
        template = loader.get_template('posts/usernamepage.html')
        # Load up the data into a context.
        context = {
            'latestPosts': latestPosts,
            'userInfo': userInfo,
            'isPageOwner': False,
            'loggedIn': False,
            }
        # And go!
        return HttpResponse(template.render(context, request))
