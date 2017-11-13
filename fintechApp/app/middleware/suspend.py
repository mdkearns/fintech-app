from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from re import compile

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings,'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

# class Suspend(MiddlewareMixin):
#     def process_request(self, request):
#         assert hasattr(request, 'user'), "middleware must be installed"
#         response = self.get_response(request)
#         if not request.user.is_authenticated():
#             path = request.path_info.lstrip('/')
#             if not any(m.match(path) for m in EXEMPT_URLS):
#             return HttpResponseRedirect('login')
#         return response
class Suspend(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/app/':
            return None
        if request.path.startswith('/app/create_user/'):
            return None
        if request.path.startswith('/accounts/'):
            return None
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        if request.user.is_authenticated() and request.user.profile.suspended:
            print('suspended')
            return HttpResponseRedirect(reverse('index'))
        return None
