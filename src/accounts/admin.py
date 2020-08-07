from django.contrib import admin
from accounts.models import UserDetails, Followers

admin.site.register(UserDetails)
admin.site.register(Followers)
