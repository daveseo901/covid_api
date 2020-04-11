from rest_framework.pagination import PageNumberPagination

class ThePagination(PageNumberPagination):
    page_size_query_param = 'limit'
