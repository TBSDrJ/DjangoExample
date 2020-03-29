"""twit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

### Python version 3.7.4
### Django version 3.0.3

from django.contrib import admin
from django.urls import include, path

# I'm using function views instead of class-based views
# I had to put the admin links first because of a conflict between
#   'admin' to get the admin page vs. 'admin' to get the admin user's
#   twit page.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin', admin.site.urls),
    path('', include('posts.urls')),
    path('twit/', include('posts.urls')),
]
