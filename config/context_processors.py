from django.conf import settings

def default_image(request):
    if settings.DEBUG:
        image_url = str(settings.IMAGE_URL) + 'noImage.jpg'
    else:
        image_url = str(settings.IMAGE_URL) + 'assets/img/noImage.jpg'

    return {'DEFAULT_IMAGE': image_url}