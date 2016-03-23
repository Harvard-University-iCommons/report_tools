from django.conf.urls import url
# from django.contrib import admin

from account_courses import views as ac_views

urlpatterns = [
    #  url(r'^admin/', admin.site.urls),
    url(r'^$', ac_views.index, name='home'),
    url(r'^main$', ac_views.main, name='main'),
    url(r'^lti_launch$', ac_views.lti_launch, name='lti_launch'),
    url(r'^tool_config$', ac_views.tool_config, name='tool_config'),
]
