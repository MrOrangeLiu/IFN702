from django.contrib import admin
from .models import File, Profile, Directory, ResultFile

# Customized Admin
# @admin.register(File)
# class FileAdmin(admin.ModelAdmin):
# 	list_display = ("id", "file_name", "file_path", "file_content", "author", "created_time", "last_updated_time")

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
# 	list_display = ("id", "name", "password", "email", "sex", "created_time")

admin.site.register([File, Profile, Directory, ResultFile])