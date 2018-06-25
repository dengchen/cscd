"""cscd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from cscdapp.views import test
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^hello/', login),
    # url(r'^index',Index),
    # url(r'^Single_people1/',Single_people1 ),
    # url(r'^Single_people2/',Single_people2 ),
    # url(r'^Single_people3/',Single_people3 ),
    # url(r'^Single_people4/',Single_people4 ),
    # url(r'^Single_people5/',Single_people5 ),
    # url(r'^Single_people6/',Single_people6 ),
    # url(r'^Single_people7/',Single_people7 ),
    # url(r'^Single_people8/',Single_people8 ),
    url(r'^test/',test ),
]
