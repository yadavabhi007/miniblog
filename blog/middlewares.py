from django.shortcuts import HttpResponse
class UnderConstructionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = HttpResponse('Under Construction')
        return response