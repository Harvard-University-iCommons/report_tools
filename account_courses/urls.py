from django.conf.urls import patterns, url


urlpatterns = patterns('',

    url(r'^$', 'account_courses.views.index'),

    url(r'^lti_launch$', 'account_courses.views.lti_launch', name='lti_launch'),

    url(r'^main$', 'account_courses.views.main', name='main'),

    url(r'^tool_config$', 'account_courses.views.tool_config', name='tool_config'),

    url(r'^oauth_complete$', 'account_courses.views.oauth_complete', name='oauth_complete'),

)

