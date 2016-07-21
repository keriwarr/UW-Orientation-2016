from django.contrib import admin

import apps.announcements.models as models


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    search_fields = ('title',)
