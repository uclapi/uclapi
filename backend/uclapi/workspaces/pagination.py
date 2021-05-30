from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class HistoricalListCursorPagination(CursorPagination):
    ordering = "datetime"

    def get_paginated_response(self, data, **kwargs):
        return Response({
            "okay": True,
            "data": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data
            }
        })
