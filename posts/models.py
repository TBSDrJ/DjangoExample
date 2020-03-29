
### Python version 3.7.4
### Django version 3.0.3

from django.db import models


class Post(models.Model):
    """
    This model will contain the data for a single post to Twit.
    """
    postText = models.CharField(max_length=280)
    # This matches up with the 'username' field of the built-in User model.
    userPosted = models.CharField(max_length=50)
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
