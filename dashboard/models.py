from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    """
    Extended user profile model to store additional user information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone Number'))
    address = models.TextField(blank=True, null=True, verbose_name=_('Address'))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('City'))
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Country'))
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Postal Code'))
    about_me = models.TextField(blank=True, null=True, verbose_name=_('About Me'))
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name=_('Profile Picture'))
    
    # Social Media Links
    twitter_url = models.URLField(blank=True, null=True, verbose_name=_('Twitter URL'))
    facebook_url = models.URLField(blank=True, null=True, verbose_name=_('Facebook URL'))
    instagram_url = models.URLField(blank=True, null=True, verbose_name=_('Instagram URL'))
    linkedin_url = models.URLField(blank=True, null=True, verbose_name=_('LinkedIn URL'))
    
    # Additional Fields
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('Date of Birth'))
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', _('Male')),
            ('female', _('Female')),
            ('other', _('Other')),
            ('prefer_not_to_say', _('Prefer not to say'))
        ],
        blank=True,
        null=True,
        verbose_name=_('Gender')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username


class Notification(models.Model):
    """
    Model to store user notifications.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    message = models.TextField(verbose_name=_('Message'))
    is_read = models.BooleanField(default=False, verbose_name=_('Is Read'))
    notification_type = models.CharField(
        max_length=20,
        choices=[
            ('info', _('Information')),
            ('success', _('Success')),
            ('warning', _('Warning')),
            ('error', _('Error')),
            ('primary', _('Primary')),
            ('secondary', _('Secondary'))
        ],
        default='info',
        verbose_name=_('Notification Type')
    )
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Icon'))
    url = models.URLField(blank=True, null=True, verbose_name=_('URL'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class UserActivity(models.Model):
    """
    Model to track user activities.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=100, verbose_name=_('Activity Type'))
    details = models.JSONField(blank=True, null=True, verbose_name=_('Details'))
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('IP Address'))
    user_agent = models.TextField(blank=True, null=True, verbose_name=_('User Agent'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    
    class Meta:
        verbose_name = _('User Activity')
        verbose_name_plural = _('User Activities')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.created_at}"


# Signal to create a profile when a new user signs up
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a profile for each new user.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the profile when the user is saved.
    """
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # In case the profile wasn't created by the create signal
        Profile.objects.create(user=instance)
