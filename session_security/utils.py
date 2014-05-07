""" Helpers to support json encoding of session data """

from datetime import datetime


def set_last_activity(session, dt):
    """ Set the last activity datetime as a string in the session. """
    session['_session_security'] = dt.isoformat()


def get_last_activity(session):
    """
    Get the last activity datetime string from the session and return the
    python datetime object.
    """
    return datetime.strptime(session['_session_security'],
        '%Y-%m-%dT%H:%M:%S.%f')


def lock_session(session):
    """
    Set the locked flag in the session.
    """
    session['_session_locked'] = True


def unlock_session(session):
    """
    Clear the locked flag in session.
    """
    if '_session_locked' in session:
        del session['_session_locked']


def is_locked(session):
    """
    Check if the session is locked.
    """
    if '_session_locked' in session and session['_session_locked']:
        return True
    return False
