from . import models

# A function to add a website logo through the admin panel
def get_logo(request):
    logo = models.AppSetting.objects.first()
    data = {
        'logo': logo.image_tag
    }
    return data