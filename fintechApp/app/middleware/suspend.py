from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from re import compile

class Suspend(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/app/':
            return None
        if request.path.startswith('/app/create_user/'):
            return None
        if request.path.startswith('/admin/'):
            return None
        if request.path.startswith('/accounts/'):
            return None
      #  if not request.user.is_authenticated():
      #      return HttpResponseRedirect(reverse('login'))
        if request.user.is_authenticated() and request.user.profile.suspended:
            return HttpResponseRedirect(reverse('index'))
        return None
