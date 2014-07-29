from django import template

register = template.Library()

CANVAS_VIEWS = {
    'feed': 'Recent Activity',
    'wiki': 'Wiki Front Page',
    'modules': 'Course Modules Page',
    'assignments': 'Assignment List',
    'syllabus': 'Course Syllabus Page',
}

@register.filter
def get_view_name(key):
    return CANVAS_VIEWS.get(key, key)
