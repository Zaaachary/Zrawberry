from django.contrib import admin
from .models import UserProfile, UserInfo


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth', 'wechat')     # 列出列表内的项目
    list_filter = ('wechat',)                      # 规定网页右边FILTER的显示内容


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty')
    list_filter = ('specialty',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserInfo, UserInfoAdmin)


