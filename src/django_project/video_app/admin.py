from django.contrib import admin

from src.django_project.video_app.models import VideoModel, VideoMediaModel


class VideoAdmin(admin.ModelAdmin):
    pass


class VideoMediaAdmin(admin.ModelAdmin):
    pass


admin.site.register(VideoModel, VideoAdmin)

admin.site.register(VideoMediaModel, VideoMediaAdmin)
