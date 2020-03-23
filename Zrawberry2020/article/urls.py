from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

app_name = "article"

urlpatterns = [
    # 后台
    path('article-column/', views.article_column, name="article_column"),
    path('article-post/', views.ArticlePostView.as_view(), name="article_post"),
    path('article-list/', views.article_list, name="article_list"),
    re_path('article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$',
            views.article_detail, name="article_detail"),

    # 后台功能
    path('del-article/', views.del_article, name="del_article"),
    path('delete-column/', views.delete_article_column, name="del_article_column"),
    path('redit-article/<int:pk>/<slug:slug>/', views.ArticleEditView.as_view(), name="redit_article"),
    path('rename-column/', views.rename_article_column, name="rename_article_column"),

    # 前台
    path('', views.article_titles, name="article_titles"),
    path('timeline/', views.TimelineView.as_view(), name="timeline"),
    path('dessert/', views.dessert, name="dessert"),
    path('<column_name>/', views.article_titles, name="article_column"),
    path('article-content/<int:aid>/<slug:slug>/', views.article_content, name="article_content"),
]
