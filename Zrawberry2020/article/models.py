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


class ArticleTag(models.Model):
    tag = models.CharField(max_length=30, blank=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tag


class ArticlePost(models.Model):
    SHOW_TYPE = [('0', '文章'), ('1', '甜品站'), ('2', '特殊页面')]
    # author, title, slug, column, body, created, updated,viewed, showtype,targetuser,tags

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(verbose_name="标题", max_length=200)
    column = models.ForeignKey(ArticleColumn, verbose_name="栏目", on_delete=models.PROTECT,
                               related_name="article", null=True, blank=True)
    tags = models.ManyToManyField(ArticleTag, verbose_name="标签", blank=True, related_name="Articles")
    body = models.TextField(verbose_name="正文")
    showtype = models.CharField(verbose_name="展示类型", max_length=10, choices=SHOW_TYPE, default='0')
    targetuser = models.ManyToManyField(User, verbose_name="目标用户(甜品站)",
                                        related_name="dessert", blank=True)

    slug = models.SlugField(max_length=500)
    created = models.DateTimeField(default=timezone.now)  # 时区的发布时间
    updated = models.DateTimeField(default=timezone.now)
    viewed = models.IntegerField(default=0)

    # users_like = models.ManyToManyField(User, related_name="articles_like", blank=True)
    # article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True)

    class Meta:
        ordering = ("-updated",)
        index_together = (('id', 'slug'),)  # 使用两个字段建立索引 加快读取速度
        permissions = (
            ("get_dessert", "可以进入甜品站，查看以自己为对象的文章。"),
            ("post_article", "发布或者编辑文章"),
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kargs):
        """重写save方法"""
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):
        # 后台的文章页面
        return reverse("article:article_detail", args=[self.id, self.slug])

    def get_url_path(self):
        return reverse("article:article_content", args=[self.id, self.slug])

    @classmethod
    def get_special_page(cls):
        pages = cls.objects.filter(showtype='2')
        return {'special_page': pages}


class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name="comments")
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "{0}在{1}中发表".format(self.commentator.username, self.article)


class Navlink(models.Model):
    name = models.CharField(max_length=12, verbose_name="链接名")
    link = models.CharField(max_length=100, default='/article/', verbose_name="链接")
    show = models.BooleanField(default=True, verbose_name="展示")

    def __str__(self):
        return self.name

    @classmethod
    def get_nav_link(cls):
        nav_links = cls.objects.filter(show=True)
        return {'nav_links': nav_links}
