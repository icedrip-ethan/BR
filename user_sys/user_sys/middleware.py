import re
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout


# create list of URL's for comparison 
EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
	EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def process_view(self, request, view_func, view_args, view_kwargs):
		assert hasattr(request, 'user')
		#url that user is requesting
		path = request.path_info.lstrip('/')
		print(path)
		#user is trying to acess a url that doesn't require login
		url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
		if path == reverse('accounts:logout').lstrip('/') and request.user.is_authenticated():
			return logout(request)
		if request.user.is_authenticated() and url_is_exempt:
			return redirect(settings.LOGIN_REDIRECT_URL)
		elif request.user.is_authenticated() or url_is_exempt:
			return None
		# e.g. not authenticated and requesting a non-exempt url
		else:
			return redirect(settings.LOGIN_URL)
