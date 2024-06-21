from django.http import HttpResponseForbidden

class URLBlockMiddleware:
    #BLOCKED_URLS = '/video/'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print(f"Blocked URLs: {self.BLOCKED_URLS}")
        print(f"Requested path: {request.path}")
        if request.path.startswith(self.BLOCKED_URLS):
            return HttpResponseForbidden("Accesso negato a questa risorsa.")
        return self.get_response(request)