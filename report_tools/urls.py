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
from django.conf.urls import include, url

from icommons_ui import views as ui_views

from account_courses import views as ac_views

urlpatterns = [
    url(r'^account_courses/', include('account_courses.urls', 'ac')),
    url(r'^auth_error/', ui_views.not_authorized, name='lti_auth_error'),
    url(r'^not_authorized/', ui_views.not_authorized, name='not_authorized'),
    url(r'^oauth/complete', ac_views.oauth_complete, name='oauth_complete'),
]
