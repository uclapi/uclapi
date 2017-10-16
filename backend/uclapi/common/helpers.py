from django.http import JsonResponse


class PrettyJsonResponse(JsonResponse):
    def __init__(self, data, rate_limiting_data=None):
        # Calls JsonResponse's constructure and requests 4 line indenting
        super().__init__(data, json_dumps_params={'indent': 4})

        # Adds rate limiting headers from a passed view kwargs
        if rate_limiting_data:
            if 'X-RateLimit-Limit' in rate_limiting_data:
                self['X-RateLimit-Limit'] = rate_limiting_data['X-RateLimit-Limit']
            if 'X-RateLimit-Remaining' in rate_limiting_data:
                self['X-RateLimit-Remaining'] = rate_limiting_data['X-RateLimit-Remaining']
            if 'X-RateLimit-Retry-After' in rate_limiting_data:
                self['X-RateLimit-Retry-After'] = rate_limiting_data['X-RateLimit-Retry-After']
