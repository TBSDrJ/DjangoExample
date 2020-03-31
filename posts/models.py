
### Python version 3.7.4
### Django version 3.0.3

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """
    This model will contain the posts to the Twit platform.

    It is an update of an earlier version that used just the username of
    the poster in userPosted instead of the User object.
    """
    postText = models.CharField(max_length=280)
    # This links to the built-in User model.
    userPosted = models.ForeignKey(User, on_delete=models.CASCADE)
    pubDate = models.DateTimeField('date published')
    likes = models.IntegerField(default=0)

    def __str__(self):
        # I'm using a more complete stringification of the Post that shows
        # the first 40 characters of the text, the id number of the post, and
        # the time/date it was published.
        postStr = "\n\t" + "Id: " + str(self.id)
        if len(self.postText) < 40:
            postStr += "\n\t" + "postText: " + self.postText
        else:
            postStr += "\n\t" + "postText: " + self.postText[:40] + "..."
        postStr += "\n\t" + "Date Published: " + str(self.pubDate)
        postStr += "\n"
        return postStr

# class Profile(models.Model):
#     """
#     This model extends the built-in User model using a OneToOne relationship.
#     """
#     # Set up the one-to-one relationship with the User model
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         primary_key=True
#     )
#     verified = models.BooleanField(default=False)
#     # If you want to allow a Text or CharField to be empty, use this pairing
#     #   of default="" and blank=True instead of null=True.
#     #   c.f.: https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.Field.null
#     bio = models.TextField(default="", blank=True)
#     location = models.CharField(max_length=100, default="", blank=True)
