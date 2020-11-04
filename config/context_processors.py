from django.conf import settings

def image_url(request):
    return {'IMAGE_URL': settings.IMAGE_URL}