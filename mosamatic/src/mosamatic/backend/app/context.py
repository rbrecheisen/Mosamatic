def version(request):
    from django.conf import settings
    return {'VERSION': settings.VERSION}