
### Python version 3.7.4
### Django version 3.0.3

from django.urls import path
from . import views

# I might get rid of loading up user pages by ID, it really is not necesary.
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('<username>/followed', views.FollowedView.as_view(), name="followed"),
    path('<username>', views.UsernameView.as_view(), name="username"),
]
