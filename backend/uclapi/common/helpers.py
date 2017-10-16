from django.http import JsonResponse

class PrettyJsonResponse(JsonResponse):
    def __init__(self, data):
        super().__init__(data, json_dumps_params={'indent': 4})
