from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import *

admin.site.site_header = 'tinbox Admin'

admin.site.register(Slide)
admin.site.register(Slideshow, GuardedModelAdmin)
admin.site.register(SlideTemplates)
admin.site.register(Screen)