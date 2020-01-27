from django.contrib import admin
from .models import ArticleColumn


class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'created')
    list_filter = ('user',)


admin.site.register(ArticleColumn, ArticleColumnAdmin)
