""" One view method for AJAX requests by SessionSecurity objects. """
import time

from datetime import datetime, timedelta

from django.contrib import auth
from django.views import generic
from django import http

from .utils import get_last_activity, lock_session, unlock_session

__all__ = ['PingView', 'LockView', ]


class PingView(generic.View):
    """
    This view is just in charge of returning the number of seconds since the
    'real last activity' that is maintained in the session by the middleware.
    """

    def get(self, request, *args, **kwargs):
        if '_session_security' not in request.session:
            # It probably has expired already
            return http.HttpResponse('"logout"',
                                     content_type='application/json')

        last_activity = get_last_activity(request.session)
        inactive_for = (datetime.now() - last_activity).seconds
        return http.HttpResponse(inactive_for,
                                 content_type='application/json')


class LockView(generic.View):
    """
    This view is in charge of locking and unlocking the user session.
    """

    def get(self, request, *args, **kwargs):
        """
        Getting the view locks the session so that user must input password
        to unlock it.
        """
        if '_session_security' not in request.session:
            # It probably has expired already
            return http.HttpResponse('"logout"',
                                     content_type='application/json')

        lock_session(request.session)
        return http.HttpResponse('"locked"',
                                 content_type='application/json')

    def post(self, request, *args, **kwargs):
        """
        Posting the view unlocks the session if user provided password in the
        session is correct.
        """
        if '_session_security' not in request.session:
            # It probably has expired already
            return http.HttpResponse('"logout"',
                                     content_type='application/json')

        password = request.POST.get('session_security_password', None)
        if request.user.is_authenticated() and request.user.check_password(password):
            unlock_session(request.session)
            return http.HttpResponse('"unlocked"',
                                     content_type='application/json')

        return http.HttpResponse('"locked"',
                                 content_type='application/json')
