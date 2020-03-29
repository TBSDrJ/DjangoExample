
### Python version 3.7.4
### Django version 3.0.3

from django.contrib import admin
# I didn't do much with this, I just imported my one model
from .models import Post

admin.site.register(Post)
