from django.contrib import admin
from .models import Contact


admin.site.site_header = "codingBlog Admin"
admin.site.site_title = "codingBlog Admin Panel"
admin.site.index_title = "Welcome to codingBlog Admin Panel"

# Register your models here.
admin.site.register(Contact)
