from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class TripPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 8

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "page_size": self.page_size,
                "total_pages": self.page.paginator.num_pages,
                "count": self.page.paginator.count,
                "results": data,
            }
        )
