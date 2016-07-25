import django.forms as forms
import django.contrib.admin as admin

import teams.models as models
import users.models


@admin.register(models.TeamCheer)
class TeamCheerAdmin(admin.ModelAdmin):
    pass

@admin.register(models.TeamProfile)
class TeamProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    pass
