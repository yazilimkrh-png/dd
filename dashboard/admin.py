from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Profile, Notification, UserActivity


class ProfileInline(admin.StackedInline):
    """Inline admin for the Profile model."""
    model = Profile
    can_delete = False
    verbose_name_plural = _('Profile')
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    """Custom User Admin with Profile inline."""
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone')
    list_select_related = ('profile', )
    
    def get_phone(self, instance):
        return instance.profile.phone
    get_phone.short_description = _('Phone')
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin for the Notification model."""
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        (_('Notification Details'), {
            'fields': ('user', 'title', 'message', 'notification_type', 'is_read')
        }),
        (_('Additional Information'), {
            'fields': ('icon', 'url'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin for the UserActivity model."""
    list_display = ('user', 'activity_type', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__username', 'activity_type', 'details')
    readonly_fields = ('created_at', 'user', 'activity_type', 'details', 'ip_address', 'user_agent')
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    fieldsets = (
        (_('Activity Details'), {
            'fields': ('user', 'activity_type')
        }),
        (_('Technical Information'), {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        (_('Additional Data'), {
            'fields': ('details',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
