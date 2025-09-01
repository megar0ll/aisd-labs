from django.contrib import admin
from .models import AboutImage, ContactMessage

@admin.register(AboutImage)
class AboutImageAdmin(admin.ModelAdmin):
    list_display = ['caption', 'created_at']
    list_filter = ['created_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']