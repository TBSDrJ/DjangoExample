
### Python version 3.7.4
### Django version 3.0.3

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Custom imports added
# Add my model
from .models import Post
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
    # Early stage of development
    return HttpResponse("Followed Page")

def usernamepage(request, username):
    # Use the Pretty Printer to make this giant mess vaguely readable.
    # Notice that the vars() function means I see *all* of the dictionary
    #   instead of just the __str()__ method version of it.
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(vars(request))

    # This page has a form to add a post that redirects to itself, so check if
    #   that form was filled out or not.
    if request.POST:
        # Create an instance of the Post object.
        newPost = Post(
            postText = request.POST['newPostText'],
            userPosted = request.POST['userPosting'],
            pubDate = timezone.now(),
            )
        # Save to the database.
        newPost.save()
    # Make sure that this user exists before we get the user info.
    # Show error page if user does not exist.
    try:
        userInfo = User.objects.filter(username=username)[0]
    except:
        template = loader.get_template('posts/nosuchusername.html')
        context = {
            'username': username,
            }
        return HttpResponse(template.render(context, request))
    # Get all the posts for this user only *after* we've added the new one if that happened.
    myPosts = Post.objects.filter(userPosted = userInfo.id)
    # Now, cut this down to the most recent and put in order
    latestPosts = myPosts.order_by('-pubDate')[:5]
    # Go find the template
    template = loader.get_template('posts/usernamepage.html')
    # Load up the data into a context.
    context = {
        'latestPosts': latestPosts,
        'username': userInfo.username,
        'firstName': userInfo.first_name,
        'lastName': userInfo.last_name,
        'user': username,
        }
    # And go!
    return HttpResponse(template.render(context, request))

def useridpage(request, id):
    # Find the user
    thisUser = User.objects.filter(id=id)
    # Check if we found something.
    # If not, show an error page.
    try:
        userInfo = User.objects.filter(id=id)[0]
    except:
        template = loader.get_template('posts/nosuchuserid.html')
        context = {
            'userid': id,
            }
        return HttpResponse(template.render(context, request))
    # Find the user's posts
    myPosts = Post.objects.filter(userPosted = id)
    # Grab the most recent five
    latestPosts = myPosts.order_by('-pubDate')[:5]
    # Find the data
    template = loader.get_template('posts/useridpage.html')
    # Line up the data for the context
    context = {
        'latestPosts': latestPosts,
        'userid': userInfo.id,
        'username': userInfo.username,
        'firstName': userInfo.first_name,
        'lastName': userInfo.last_name,
        }
    # And go!
    return HttpResponse(template.render(context, request))
