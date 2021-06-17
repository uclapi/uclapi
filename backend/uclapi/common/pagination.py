from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data, **kwargs):
        return Response({
            "okay": True,
            self.request.path.split("/")[-1]: {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "results": data
            }
        })
