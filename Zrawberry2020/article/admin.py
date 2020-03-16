from django.contrib import admin
from .models import ArticleColumn, ArticlePost, Comment, ArticleTag


class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'created')
    list_filter = ('user',)


class ArticleTagsAdmin(admin.ModelAdmin):
    list_display = ('tag', 'created')
    # list_filter = ('created',)


class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'created', 'showtype')
    list_filter = ('column',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentator', 'body', 'article', 'created')
    list_filter = ('article', 'created',)


admin.site.register(ArticleColumn, ArticleColumnAdmin)
admin.site.register(ArticleTag, ArticleTagsAdmin)
admin.site.register(ArticlePost, ArticlePostAdmin)
admin.site.register(Comment, CommentAdmin)

