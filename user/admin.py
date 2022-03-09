from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SignupForm, CustomUserChangeForm
from .models import UserDetails


class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    form = CustomUserChangeForm
    model = UserDetails
    list_display = ('netid', 'is_staff', 'is_active',)
    list_filter = ('netid', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('netid', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('netid', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('netid',)
    ordering = ('netid',)


admin.site.register(UserDetails, CustomUserAdmin)