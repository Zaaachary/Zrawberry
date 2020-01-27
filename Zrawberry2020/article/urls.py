from django.urls import path, re_path
from . import views

app_name = "article"

urlpatterns = [
    path('', views.article_titles, name="article_titles"),
    path('article-column/', views.article_column, name="article_column"),
    path('article-post/', views.article_post, name="article_post"),
    path('article-list/', views.article_list, name="article_list"),
    path('del-articlde/', views.del_article, name="del_article"),
    path('delete-column/', views.delete_article_column, name="del_article_column"),
    path('redit-article/<int:article_id>/', views.redit_article, name="redit_article"),
    path('rename-column/', views.rename_article_column, name="rename_article_column"),
    re_path('article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$',
            views.article_detail, name="article_detail"),
    path('article-content/<int:id>/<slug:slug>/', views.article_content, name="article_content"),
]