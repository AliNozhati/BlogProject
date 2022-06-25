from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

# تغییر دادن لیست فیلد های پنل ادمین

# UserAdmin.fieldsets += (
#     ("فیلد های خاص من", {'fields': ('is_author', 'special_user')}),
# )
UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active', 
    'is_staff', 
    'is_superuser',
    'is_author',
    'special_user',
    'groups', 
    'user_permissions',
)

UserAdmin.list_display += ('is_author', 'is_special_user')

admin.site.register(User, UserAdmin)