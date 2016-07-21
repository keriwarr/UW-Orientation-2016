from django.contrib import admin

import users.models as models


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'first_name')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('password', )
        form = super(CustomUserAdmin, self).get_form(request, obj, **kwargs)
        return form
