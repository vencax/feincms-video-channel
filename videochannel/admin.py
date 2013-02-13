from django.contrib import admin

from .models import Video
from .forms import MyVideoAdminForm


class VideoAdmin(admin.ModelAdmin):

    list_display = ('mediaFile', 'subtitles')
    search_fields = ('mediaFile__translation__title', 'subtitles')
    form = MyVideoAdminForm

admin.site.register(Video, VideoAdmin)
