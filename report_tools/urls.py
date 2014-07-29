from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_name.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^reports/account_courses/', include('account_courses.urls', namespace='ac')),
    url(r'^reports/auth_error/', 'icommons_ui.views.not_authorized', name='lti_auth_error'),
    url(r'^reports/not_authorized/', 'icommons_ui.views.not_authorized', name='not_authorized'),

)
