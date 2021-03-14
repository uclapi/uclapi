from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # In the majority of cases we can simplify the error to just
        # return the detail (i.e. string) of the error.
        if "detail" in response.data:
            response = Response({
                "okay": False,
                "error": response.data["detail"]
            }, status=response.status_code)
        else:
            # For Django Rest Framework date time ranges it does not
            # use the detail key
            response = Response({
                "okay": False,
                "error": response.data
            }, status=response.status_code)

    return response
