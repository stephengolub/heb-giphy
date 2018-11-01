from django.contrib import admin

from .models import Gif, Tag, TagSource


admin.site.register(Gif)
admin.site.register(Tag)
admin.site.register(TagSource)
