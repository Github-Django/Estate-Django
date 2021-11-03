from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser


# Register your models here.

UserAdmin.fieldsets += (
    ('وضعیت نمایندگی', {'fields': ('is_author',)}),
)
UserAdmin.list_display += (
    "is_author",
)


# class MyUserAdmin(admin.ModelAdmin):
#     model = MyUser
#     list_display = ('first_name', 'last_name','phone')
#     # list_filter = ()
#     # search_fields = ()
#     # ordering = ()
#     # filter_horizontal = ()
#     # fieldsets = UserAdmin.fieldsets + (
#     #     ('وضعیت نمایندگی', {'fields': ('is_author',)}),
#     # )


admin.site.register(MyUser)

