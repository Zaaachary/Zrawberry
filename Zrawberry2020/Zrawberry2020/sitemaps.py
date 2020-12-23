from django.contrib.sitemaps import Sitemap
from article.models import ArticlePost       # model

class BlogSitemap(Sitemap):
    changefreq = "monthly"        # 修改频率
    # changefreq = "never"        # 修改频率
    priority = 0.5    # https://www.sitemaps.org/protocol.html#prioritydef

    def items(self):
        # 返回的结果会跑到其他的函数里作为 obj
        return ArticlePost.objects.filter(showtype='0') # 获取合法 item

    def lastmod(self, obj):
        return obj.updated     # 发布日期

    def location(self, obj):
        # 默认会返回 get_absolute_url 那个是后台的url
        return obj.get_url_path()   