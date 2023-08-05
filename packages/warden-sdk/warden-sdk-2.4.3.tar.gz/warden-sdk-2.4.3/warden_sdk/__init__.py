"""Initialization of the `warden_sdk`.

Here we include all of the relevant and necessary features and functions for the `warden_sdk` to run properly and that the user is allowed to use.

  Typical usage example:

  import warden_sdk
  from warden_sdk.integrations import FlaskIntegrations
  
  warden_sdk.init(
    creds=('client_id','client_secret'),
    service='clerk',
    api='datastore'
    scopes=['scope.1'],
    integrations=[FlaskIntegration()]
  )

Code reference:
- [warden_sdk](https://github.com/getwarden/warden-python/blob/master/warden_sdk/__init__.py)
"""

from warden_sdk.hub import Hub, init
from warden_sdk.scope import Scope
from warden_sdk.transport import Transport, HttpTransport
from warden_sdk.client import Client

from warden_sdk.auth.oauth import OAuth2
from warden_sdk.auth.user import User as U

from warden_sdk.auth.headers import *    # noqa

User = U()

from warden_sdk.auth.scope_guard import ScopeGuard as SG

ScopeGuard = SG()

from warden_sdk.api import *    # noqa

from warden_sdk.consts import VERSION

__version__ = VERSION

__title__ = "Warden"
__description__ = "Warden SDK for Python language."
__url__ = "https://github.com/theferant/warden-sdk-py"
__uri__ = __url__
__doc__ = __description__ + " <" + __uri__ + ">"

__author__ = "Ferant Tech Corporation"
__email__ = "mpodsiadly@ferant.io"

__license__ = "MIT"
__copyright__ = "Copyright 2021 Ferant Tech Corporation"

__all__ = [
    "Hub",
    "Client",
    "Transport",
    "HttpTransport",
    "init",
    "integrations",
    "OAuth2",
    "User",
    "ScopeGuard",
    # From warden_sdk.auth.headers
    "add_secure_headers",
    "check_ssl_cert",
    "check_referrer",
    "cors_list",
    # From warden_sdk.api
    "debug",
    "set_test_user"
    "capture_event",
    "capture_message",
    "capture_exception",
    "add_breadcrumb",
    "configure_scope",
    "push_scope",
    "flush",
    "last_event_id",
    "start_span",
    "start_transaction",
    "set_tag",
    "set_context",
    "set_extra",
    "set_user",
    "set_level",
]

# Initialize the debug support after everything is loaded
from warden_sdk.debug import init_debug_support

init_debug_support()
del init_debug_support
