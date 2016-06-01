from django.contrib import admin
import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass
