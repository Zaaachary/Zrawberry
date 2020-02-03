from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from slugify import slugify


class ArticleColumn(models.Model):
    """文章栏目"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_column')
    column = models.CharField(max_length=50)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, on_delete=models.PROTECT, related_name="article", blank=True)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)  # 时区的发布时间
    updated = models.DateTimeField(auto_now=True)
    viewed = models.IntegerField(default=0)

    # users_like = models.ManyToManyField(User, related_name="articles_like", blank=True)
    # article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True)

    class Meta:
        ordering = ("-updated",)
        index_together = (('id', 'slug'),)  # 使用两个字段建立索引 加快读取速度

    def __str__(self):
        return self.title

    def save(self, *args, **kargs):
        """重写save方法"""
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id, self.slug])

    def get_url_path(self):
        return reverse("article:article_content", args=[self.id, self.slug])
