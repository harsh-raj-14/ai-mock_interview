from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import timedelta


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            last_activity_value = request.session.get('last_activity')

            if isinstance(last_activity_value, str):
                last_activity = parse_datetime(last_activity_value)
            else:
                last_activity = None

            if last_activity:
                if timezone.is_naive(last_activity):
                    last_activity = timezone.make_aware(last_activity)

                timeout = timedelta(minutes=settings.AUTO_LOGOUT_MINUTES)
                if now - last_activity > timeout:
                    logout(request)
                    return redirect('login')

            request.session['last_activity'] = now.isoformat()

        return self.get_response(request)
