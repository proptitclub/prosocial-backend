from rest_framework.pagination.PageNumberPagination


class SmallResultSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 30