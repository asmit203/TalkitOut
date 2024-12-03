from django.utils import timezone

class LastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.profile.lastseen = timezone.now()
            request.user.profile.save()
        return self.get_response(request)