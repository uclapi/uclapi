import ciso8601
import datetime
import pytz
import re
import redis

from datetime import timezone
from email.utils import format_datetime
from functools import wraps

from dashboard.models import App, APICall

from oauth.models import OAuthToken
from oauth.scoping import Scopes

from .helpers import PrettyJsonResponse as JsonResponse

from uclapi.settings import REDIS_UCLAPI_HOST


# Gets a variable from GET or POST not caring which is which
def get_var(request, var_name):
    if var_name in request.GET:
        return request.GET[var_name]
    elif var_name in request.POST:
        return request.POST[var_name]
    else:
        return None


class UclApiIncorrectDecoratorUsageException(Exception):
    pass


class UclApiIncorrectTokenTypeException(Exception):
    pass


def how_many_seconds_until_midnight():
    """Returns the number of seconds until midnight."""
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    midnight = datetime.datetime(
        year=tomorrow.year, month=tomorrow.month,
        day=tomorrow.day, hour=0, minute=0, second=0
    )
    return (midnight - datetime.datetime.now()).seconds


def log_api_call(request, token, token_type):
    """This functions handles logging of api calls."""
    service = request.path.split("/")[1]
    method = "/".join(request.path.split("/")[2:])

    headers = request.META
    version_headers = {}
    regex = re.compile("^HTTP_UCLAPI_.*_VERSION$")
    for header in headers:
        if regex.match(header):
            version_headers[header] = headers[header]

    queryparams = dict(request.GET)

    # token is either app or OAuthToken type. This should be changed,
    # we don't want variables that can store multiple types....

    if token_type in {"general", "oauth"}:
        # parameters = {
        #     "userid": token.user.id,
        #     "email": token.user.email,
        #     "name": token.user.given_name,
        #     "service": service,
        #     "method": method,
        #     "version-headers": version_headers,
        #     "queryparams": queryparams,
        #     "temp_token": False,
        #     "token_type": token_type
        # }
        if token_type == "general":
            call_log = APICall(app=token, user=token.user, token=None,
                               token_type=token_type, service=service,
                               method=method, queryparams=queryparams)
            call_log.save()
        else:
            call_log = APICall(app=token.app, user=token.user, token=token,
                               token_type=token_type, service=service,
                               method=method, queryparams=queryparams)
            call_log.save()

    # elif token_type == "general-temp":
    #     parameters = {
    #         "service": service,
    #         "method": method,
    #         "version-headers": version_headers,
    #         "queryparams": queryparams,
    #         "temp_token": True,
    #         "token_type": token_type
    #     }


def throttle_api_call(token, token_type):
    if token_type == 'general':
        cache_key = token.user.email
        limit = token.user.dev_quota
    elif token_type == 'general-temp':
        cache_key = token
        limit = 10
    elif token_type == 'oauth':
        cache_key = "oauth:" + token.user.email
        limit = token.user.oauth_quota
    elif token_type == 'test-token':
        cache_key = token
        limit = 1
    else:
        raise UclApiIncorrectTokenTypeException

    r = redis.Redis(host=REDIS_UCLAPI_HOST)
    count_data = r.get(cache_key)

    secs = how_many_seconds_until_midnight()
    if count_data is None:
        # Conditional fixes bug where a call is made exactly at midnight.
        # Redis cannot have key with TTL of 0
        r.set(cache_key, 1, secs if secs > 0 else 86400)
        return (False, limit, limit - 1, secs)
    else:
        count = int(count_data)
        if count >= limit:
            return (True, limit, limit - count, secs)
        else:
            r.incr(cache_key)
            return (False, limit, limit - count, secs)


def _check_oauth_token_issues(token_code, client_secret, required_scopes):
    try:
        token = OAuthToken.objects.get(token=token_code)
    except OAuthToken.DoesNotExist:
        response = JsonResponse({
            "ok": False,
            "error": "Token does not exist."
        })
        response.status_code = 400
        return response

    if token.app.client_secret != client_secret:
        response = JsonResponse({
            "ok": False,
            "error": "Client secret incorrect."
        })
        response.status_code = 400
        return response

    if not token.active:
        response = JsonResponse({
            "ok": False,
            "error":
                "The token is inactive as the user has revoked "
                "your app's access to their data."
        })
        response.status_code = 400
        return response

    if token.app.deleted:
        response = JsonResponse({
            "ok": False,
            "error":
                "The token is invalid as the developer has "
                "deleted their app."
        })
        response.status_code = 403
        return response

    scopes = Scopes()
    for s in required_scopes:
        if not scopes.check_scope(token.scope.scope_number, s):
            response = JsonResponse({
                "ok": False,
                "error":
                    "The token provided does not have "
                    "permission to access this data."
            })
            response.status_code = 400
            return response

    # Return the token as there are no issues
    return token


def _check_temp_token_issues(
    token_code,
    personal_data,
    request_path,
    page_token=None
):
    # The token is a generic one, so sanity check
    if personal_data:
        response = JsonResponse({
            "ok": False,
            "error": "Personal data requires OAuth."
        })
        response.status_code = 400
        return response

    r = redis.Redis(host=REDIS_UCLAPI_HOST)

    if not r.get(token_code):
        response = JsonResponse({
            "ok": False,
            "error": "Temporary token is either invalid or expired."
        })
        response.status_code = 400
        return response

    if request_path != "/roombookings/bookings":
        response = JsonResponse({
            "ok": False,
            "error":
                "Temporary token can only be used "
                "for /bookings."
        })
        response.status_code = 400
        return response

    if page_token:
        response = JsonResponse({
            "ok": False,
            "error":
                "Temporary token can only return one booking."
        })
        response.status_code = 400
        return response
    # No issues, so return the temporary token
    return token_code


def _check_general_token_issues(token_code, personal_data):
    # The token is a generic one, so sanity check
    if personal_data:
        response = JsonResponse({
            "ok": False,
            "error": "Personal data requires OAuth."
        })
        response.status_code = 400
        return response

    try:
        token = App.objects.get(
            api_token=token_code,
            deleted=False
        )
    except App.DoesNotExist:
        response = JsonResponse({
            "ok": False,
            "error": "Token does not exist."
        })
        response.status_code = 400
        return response

    # No issues, so return the token
    return token


def _get_last_modified_header(redis_key=None):
    # Default last modified is the UTC time now
    last_modified = format_datetime(
        datetime.datetime.utcnow().replace(tzinfo=timezone.utc),
        usegmt=True
    )

    # If we haven't been passed a Redis key, we just return the
    # current timeztamp as a last modified header.
    if redis_key is None:
        return last_modified

    # We have been given a Redis key, so attempt to pull it from Redis
    r = redis.Redis(host=REDIS_UCLAPI_HOST)
    redis_key = "http:headers:Last-Modified:" + redis_key
    value = r.get(redis_key)

    if value:
        # Convert the Redis bytes response to a string.
        value = value.decode('utf-8')

        # We need the UTC timezone so that we can convert to it.
        utc_tz = pytz.timezone("UTC")

        # Parse the ISO 8601 timestamp from Redis and represent it as UTC
        utc_timestamp = ciso8601.parse_datetime(value).astimezone(utc_tz)

        # Format the datetime object as per the HTTP Header RFC.
        # We replace the inner tzinfo in the timestamp to force it to be a UTC
        # timestamp as opposed to a naive one; this is a requirement for the
        # format_datetime function.
        last_modified = format_datetime(
            utc_timestamp.replace(tzinfo=timezone.utc),
            usegmt=True
        )

    return last_modified


def uclapi_protected_endpoint(
    personal_data=False,
    required_scopes=[],
    last_modified_redis_key='gencache'
):
    def check_request(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            # A small sanity check
            # You cannot apply a personal data scope if you are not using
            # a personal data flag
            if not personal_data:
                if required_scopes != []:
                    raise UclApiIncorrectDecoratorUsageException

            # In any case, a token should be provided
            token_code = get_var(request, 'token')
            if token_code is None:
                response = JsonResponse({
                    "ok": False,
                    "error": "No token provided."
                })
                response.status_code = 400
                return response

            if token_code.startswith('uclapi-user-'):
                # The token is an OAuth token, so apply OAuth logic
                client_secret = get_var(request, 'client_secret')
                if client_secret is None:
                    response = JsonResponse({
                        "ok": False,
                        "error": "No Client Secret provided."
                    })
                    response.status_code = 400
                    return response

                # Check for an OAuth issue.
                # If there is one, a JSONResponse will be returned from the
                # utility function. If not, it'll return the token model
                # and we can happily move on.
                oauth_check = _check_oauth_token_issues(
                    token_code,
                    client_secret,
                    required_scopes
                )
                if isinstance(oauth_check, JsonResponse):
                    return oauth_check

                token = oauth_check
                kwargs['token_type'] = 'oauth'

            elif token_code.startswith('uclapi-temp-'):
                temp_token_check = _check_temp_token_issues(
                    token_code,
                    personal_data,
                    request.path,
                    request.GET.get('page_token')
                )
                if isinstance(temp_token_check, JsonResponse):
                    return temp_token_check
                token = temp_token_check

                # This is a horrible hack to force the temporary
                # token to always return only 1 booking
                # Courtesy of: https://stackoverflow.com/a/38372217/825916
                # We make the GET data mutable first, then inject the
                # results_per_page parameter so that there can only
                # be one result returned.
                request.GET._mutable = True
                request.GET['results_per_page'] = 1

                kwargs['token_type'] = 'general-temp'

            elif token_code.startswith('uclapi-'):
                general_token_check = _check_general_token_issues(
                    token_code,
                    personal_data
                )
                if isinstance(general_token_check, JsonResponse):
                    return general_token_check

                token = general_token_check

                kwargs['token_type'] = 'general'

            else:
                # This is some type of token that we haven't seen before.
                # The user sent us a bad token.
                response = JsonResponse({
                    "ok": False,
                    "error": "Token is invalid."
                })
                response.status_code = 400
                return response

            # This should never happen. It's more of a sanity check to ensure
            # that the code above all works fine.
            if 'token_type' not in kwargs:
                raise UclApiIncorrectTokenTypeException

            kwargs['token'] = token

            # Get throttle data
            (
                throttled,
                limit,
                remaining,
                reset_secs
            ) = throttle_api_call(token, kwargs['token_type'])

            # Get last modified header
            kwargs['Last-Modified'] = _get_last_modified_header(
                last_modified_redis_key
            )

            if throttled:
                response = JsonResponse({
                    "ok": False,
                    "error": "You have been throttled. "
                             "Please try again in {} seconds."
                             .format(reset_secs)
                })
                response.status_code = 429
                response['X-RateLimit-Limit'] = limit
                response['X-RateLimit-Remaining'] = remaining
                response['X-RateLimit-Retry-After'] = reset_secs
                return response
            else:
                kwargs['X-RateLimit-Limit'] = limit
                kwargs['X-RateLimit-Remaining'] = remaining
                kwargs['X-RateLimit-Retry-After'] = reset_secs

            # Log the API call before carrying it out
            log_api_call(request, token, kwargs['token_type'])

            return view_func(request, *args, **kwargs)
        return wrapped
    return check_request
