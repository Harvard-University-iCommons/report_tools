from django.shortcuts import render, render_to_response, redirect
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from ims_lti_py.tool_config import ToolConfig
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django import template
from ims_lti_py.tool_provider import DjangoToolProvider
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from canvas_sdk.methods import accounts
from canvas_sdk import RequestContext
from canvas_sdk import client

from time import time
import logging
import requests
import urllib

logger = logging.getLogger(__name__)

TERMS = {
    '2014-1': 'Fall 2014-2015',
    '2014-2': 'Spring 2014-2015',
    '2014-5': 'Winter 2014-2015',
    '2014-4': 'Full Year 2014-2015',
}

# Create your views here.

@require_http_methods(['GET'])
def index(request):
    logger.info("request to index.")
    return render(request, 'account_courses/index.html')

@login_required
@require_http_methods(['POST'])
@csrf_exempt
def lti_launch(request):
    if request.user.is_authenticated():

        if request.session.get('canvas_api_token'):
            # we have a token, so redirect the user to the main view
            logger.debug("redirect user to the report page")
            return redirect('ac:main')

        else:
            # we need to send the user to Canvas to authorize this app and get a token
            logger.debug("session doesn't have a canvas_api_token; redirecting user to OAuth workflow")
            oauth_initial_state = '21345'
            request.session['oauth_initial_state'] = urllib.quote_plus(oauth_initial_state)  # make this some random value
            oauth_client_id = settings.REPORT_TOOLS.get('canvas_client_id')

            if request.is_secure():
                host = 'https://' + request.get_host()
            else:
                host = 'http://' + request.get_host()

            url = host + reverse('oauth_complete')

            redirect_uri = urllib.quote_plus(url)

            oauth_redir_url = 'https://%s/login/oauth2/auth?client_id=%s&response_type=code&redirect_uri=%s&state=%s' % \
                (request.session['LTI_LAUNCH'].get('custom_canvas_api_domain'), oauth_client_id, redirect_uri, oauth_initial_state)

            logger.debug('No oauth2 token - redirect the user to Canvas to get one: %s' % oauth_redir_url)
            return redirect(oauth_redir_url)

    else:
        return render(request, 'account_courses/error.html', {'message': 'Error: user is not authenticated!'}) 


@require_http_methods(['GET'])
def oauth_complete(request):

    # check for an error first
    if request.GET.get('error'):
        return render(request, 'account_courses/error.html', {'message': 'OAuth error: %s' % request.GET['error']})

    else:
        # get the code and the state
        oauth_code = request.GET.get('code')
        oauth_state = request.GET.get('state')

        # check to make sure the state value matches the one that we put into the session 
        logger.debug('oauth_initial_state is %s' % request.session.get('oauth_initial_state'))
        logger.debug('oauth workflow state is %s' % oauth_state)

        if oauth_state != request.session.get('oauth_initial_state'):
            return render(request, 'account_courses/error.html', {'message': 'OAuth state mismatch.'})
        else:
            logger.debug('User granted the tool access to the API key; now fetch the key from Canvas')

        # use the code to fetch the actual token
        # generate a post request to /login/oauth2/token
        oauth_token_url = 'https://%s/login/oauth2/token' % request.session['LTI_LAUNCH'].get('custom_canvas_api_domain')
        logger.debug('Fetch key using this URL: %s' % oauth_token_url)
        post_params = {
            'client_id': settings.REPORT_TOOLS.get('canvas_client_id'),
            'redirect_uri': reverse('oauth_complete'),
            'client_secret': settings.REPORT_TOOLS.get('canvas_client_key'),
            'code': oauth_code,
        }
        r = requests.post(oauth_token_url, post_params)

        if r.status_code == 200:
            response_data = r.json()
            canvas_api_token = response_data['access_token']
            request.session['canvas_api_token'] = canvas_api_token
            return redirect('ac:main')

        else:
            return render(request, 'account_courses/error.html', {'message': 'failed to get the token: %s' % r.text})

@login_required
@require_http_methods(['GET'])
def main(request):

    # the current account ID is in custom_canvas_account_id
    account_id = request.session['LTI_LAUNCH'].get('custom_canvas_account_id')
    account_name = request.session['LTI_LAUNCH'].get('custom_canvas_account_id')

    canvas_api_token = request.session.get('canvas_api_token')
    canvas_api_url = 'https://%s/api' % request.session['LTI_LAUNCH'].get('custom_canvas_api_domain')
    rc = RequestContext(canvas_api_token, canvas_api_url, per_page=15)

    search_term = None
    term_id = None
    published = None
    if request.GET.get('search_term'):
        if request.GET.get('search_term') == '':
            search_term = ''
        else:
            search_term = request.GET.get('search_term')

    if request.GET.get('term_id'):
        if request.GET.get('term_id') != '' and request.GET.get('term_id') != 'all':
            term_id = 'sis_term_id:%s' % request.GET.get('term_id')

    if request.GET.get('published'):
        if request.GET.get('published') == 'true' or request.GET.get('published') == 'false':
            published = request.GET.get('published')

    if request.GET.get('page_link'):
        api_response = client.get(rc, request.GET.get('page_link'))
    else:

        logger.debug('searching for "%s" and term "%s"' % (search_term, term_id))
        api_response = accounts.list_active_courses_in_account(rc, account_id, search_term=search_term, enrollment_term_id=term_id, published=published)
    
    logger.debug(api_response.text  )
    account_courses = api_response.json()
    page_links = api_response.links
    logger.debug(page_links)

    query_params = request.GET.copy()

    query_params.pop('page_link', None)
    query_string = urllib.urlencode(query_params)

    self_link = reverse('ac:main') + '?' + query_string

    canvas_hostname = request.session['LTI_LAUNCH'].get('custom_canvas_api_domain')

    return render(request, 'account_courses/main.html', {'request': request, 
        'account_courses': account_courses, 
        'page_links': page_links, 
        'search_term': request.GET.get('search_term',''), 
        'terms': TERMS, 
        'term_id': term_id, 
        'published': published, 
        'self_link': self_link,
        'canvas_hostname': canvas_hostname, })




@require_http_methods(['GET'])
def tool_config(request):

    if request.is_secure():
        host = 'https://' + request.get_host()
    else:
        host = 'http://' + request.get_host()

    url = host + reverse('ac:lti_launch')

    lti_tool_config = ToolConfig(
        title='Account Courses Report',
        launch_url=url,
        secure_launch_url=url,
    )
    # this is how to tell Canvas that this tool provides a course navigation link:
    account_nav_params = {
        'enabled': 'true',
        # optionally, supply a different URL for the link:
        # 'url': 'http://library.harvard.edu',
        'text': 'Courses in this account',
        #'default': 'disabled',
        #'visibility': 'public',
    }
    lti_tool_config.set_ext_param('canvas.instructure.com', 'account_navigation', account_nav_params)
    lti_tool_config.set_ext_param('canvas.instructure.com', 'privacy_level', 'public')
    lti_tool_config.set_ext_param('canvas.instructure.com', 'tool_id', __name__)
    lti_tool_config.description = 'This LTI tool displays the information about the courses in this account.'

    resp = HttpResponse(lti_tool_config.to_xml(), content_type='text/xml', status=200)
    return resp