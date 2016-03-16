"""report_tools URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
# from django.contrib import admin
from account_courses import views as ac_views

urlpatterns = [
    #  url(r'^admin/', admin.site.urls),
    url(r'^$', ac_views.index, name='home'),
    url(r'^main$', ac_views.main, name='main'),
    # url(r'^oauth/complete$', ac_views.oauth_complete, name='oauth_complete'),
    url(r'^lti_launch$', ac_views.lti_launch, name='lti_launch'),
    url(r'^tool_config$', ac_views.tool_config, name='tool_config'),
]
