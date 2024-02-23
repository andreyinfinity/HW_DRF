from rest_framework.pagination import PageNumberPagination


class LessonPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 20


class CoursePaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'per_page'
    max_page_size = 20

