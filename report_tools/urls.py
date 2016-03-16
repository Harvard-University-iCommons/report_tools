from django.conf.urls import include, url
from icommons_ui import views as ui_views

urlpatterns = [
    url(r'^account_courses/', include('account_courses.urls', 'ac')),
    url(r'^auth_error/', ui_views.not_authorized, name='lti_auth_error'),
    url(r'^not_authorized/', ui_views.not_authorized, name='not_authorized'),
    url(r'^oauth/', include('canvas_oauth.urls')),
]
