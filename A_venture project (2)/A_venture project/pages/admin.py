from django.contrib import admin
from .models import User,Record
#done
admin.site.register(Record)
admin.site.register(User)
admin.site.site_header = 'Algeria venture'
admin.site.site_title = 'Algeria venture'