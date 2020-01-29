from django.contrib import admin
from .models import ArticleColumn, ArticlePost


class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'created')
    list_filter = ('user',)


class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'created')
    list_filter = ('column',)


admin.site.register(ArticleColumn, ArticleColumnAdmin)
admin.site.register(ArticlePost, ArticlePostAdmin)
