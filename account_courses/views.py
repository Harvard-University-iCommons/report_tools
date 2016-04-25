from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from ims_lti_py.tool_config import ToolConfig
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from canvas_oauth.oauth import get_oauth_token

from canvas_sdk.methods import accounts
from canvas_sdk import RequestContext, client

import logging
import urllib

logger = logging.getLogger(__name__)

TERMS = {
    '2014-1': 'Fall 2014-2015',
    '2014-2': 'Spring 2014-2015',
    '2014-5': 'Winter 2014-2015',
    '2014-4': 'Full Year 2014-2015',
    '2014-0': 'Summer 2014-2015',
    '2015-1': 'Fall 2015-2016',
    '2015-2': 'Spring 2015-2016',
    '2015-5': 'Winter 2015-2016',
    '2015-4': 'Full Year 2015-2016',
    '2015-0': 'Summer 2015-2016',
}

# Create your views here.


@require_http_methods(['GET'])
def index(request):
    logger.info("request to index.")
    return render(request, 'account_courses/index.html')


@login_required
@csrf_exempt
@require_http_methods(['POST'])
def lti_launch(request):
    if request.user.is_authenticated():
        return redirect('ac:main')
    else:
        return render(request, 'account_courses/error.html', {'message': 'Error: user is not authenticated!'}) 


@login_required
@require_http_methods(['GET'])
def main(request):

    # the current account ID is in custom_canvas_account_id
    canvas_api_token = get_oauth_token(request)
    account_id = request.session['LTI_LAUNCH'].get('custom_canvas_account_id')
    account_name = request.session['LTI_LAUNCH'].get('custom_canvas_account_id')

    canvas_api_url = 'https://%s/api' % request.session['LTI_LAUNCH'].get('custom_canvas_api_domain')
    rc = RequestContext(canvas_api_token, canvas_api_url, per_page=15)

    search_term = request.GET.get('search_term')
    term_id = request.GET.get('term_id')
    published = request.GET.get('published')

    if term_id and term_id != '' and term_id != 'all':
        term_id = 'sis_term_id:%s' % term_id

    if request.GET.get('page_link'):
        api_response = client.get(rc, request.GET.get('page_link'))
    else:
        logger.debug('searching for "%s" and term "%s"' % (search_term, term_id))
        api_response = accounts.list_active_courses_in_account(rc, account_id, search_term=search_term, enrollment_term_id=term_id, published=published, per_page=12)

    logger.debug(api_response.text)
    account_courses = api_response.json()
    page_links = api_response.links
    logger.debug(page_links)

    query_params = request.GET.copy()

    query_params.pop('page_link', None)
    query_string = urllib.urlencode(query_params)

    self_link = reverse('ac:main') + '?' + query_string

    canvas_hostname = request.session['LTI_LAUNCH'].get('custom_canvas_api_domain')

    return render(request, 'account_courses/main.html', {
        'request': request,
        'account_courses': account_courses,
        'page_links': page_links,
        'search_term': request.GET.get('search_term', ''),
        'terms': TERMS,
        'term_id': term_id,
        'published': published,
        'self_link': self_link,
        'canvas_hostname': canvas_hostname,
    })


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
    }
    lti_tool_config.set_ext_param('canvas.instructure.com', 'account_navigation', account_nav_params)
    lti_tool_config.set_ext_param('canvas.instructure.com', 'privacy_level', 'public')
    lti_tool_config.set_ext_param('canvas.instructure.com', 'tool_id', __name__)
    lti_tool_config.description = 'This LTI tool displays the information about the courses in this account.'

    resp = HttpResponse(lti_tool_config.to_xml(), content_type='text/xml', status=200)
    return resp
