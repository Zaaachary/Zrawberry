from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator


from .models import ArticleColumn, ArticlePost, ArticleTag
from .forms import ArticleColumnForm, ArticlePostForm, CommentForm


# @permission_required()
@login_required
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        context = {
            "columns": columns,
            "column_form": column_form,
            "column": 'active',
        }
        return render(request, "article/column/article_column.html", context=context)

    elif request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        # 检查是否已经存在该栏目
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse("1")


@login_required()
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required()
@require_POST
@csrf_exempt
def delete_article_column(request):
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required()
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()

                # tags = request.POST['tags']
                # if tags:
                #     for atag in json.loads(tags):
                #         tag = request.user.tag.get(tag=atag)
                #         new_article.article_tag.add(tag)
                url = ArticlePost.objects.get(title=request.POST['title']).get_absolute_url()
                return HttpResponse(url)
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        # article_columns = ArticleColumn.objects.filter(user=request.user)
        article_columns = request.user.article_column.all()  # related_name
        # article_tags = request.user.tag.all()
        context = {
            "article_post_form": article_post_form,
            "article_columns": article_columns,
            # "article_tags": article_tags,
            "post": 'active',
        }
        return render(request, "article/column/article_post.html", context=context)


class ArticlePostView(CreateView):
    model = ArticlePost
    # title, column, body, showtype,targetuser
    fields = ['title', 'column', 'showtype', 'targetuser', 'body', 'tags']
    template_name = 'article/column/article_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ArticlePostView, self).dispatch(request, *args, **kwargs)


class ArticleEditView(UpdateView):
    model = ArticlePost
    fields = ['title', 'column', 'showtype', 'targetuser', 'body', 'tags']
    template_name = 'article/column/article_post.html'
    # template_name_suffix = '_update_form'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ArticleEditView, self).dispatch(request, *args, **kwargs)


@login_required()
def article_list(request):
    # articles = ArticlePost.objects.filter(author=request.user)
    # return render(request, "article/column/article_list.html", {"articles": articles})
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list, 10)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    context = {
        "articles": articles,
        "page": current_page,
        "list": 'active',
    }
    return render(request, "article/column/article_list.html", context=context)


@login_required()
def article_detail(request, id, slug):
    """从链接中获取文章信息"""
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/column/article_detail.html", {"article": article})


@login_required()
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required()
@csrf_exempt
def redit_article(request, article_id):
    if request.method == 'GET':
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        context = {
            "article": article,
            "article_columns": article_columns,
            "this_article_form": ArticlePostForm(initial={"title": article.title}),
            "this_article_column": article_column,
        }
        return render(request, "article/column/redit_article.html", context=context)
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            url = ArticlePost.objects.get(id=article_id).get_absolute_url()
            return HttpResponse(url)
        except:
            return HttpResponse("2")


def article_titles(request, column_name=None):
    articles = User.objects.get(id=1).article.filter(showtype='0')  # 只展示Zachary的
    # 获取文章列表
    if column_name:
        try:
            # articles_title = ArticleColumn.objects.get(column=column_name).article.all()
            # articles_title = ArticleColumn.objects.get(column=column_name).article.all()
            column = ArticleColumn.objects.get(column=column_name)
            articles_title = articles.filter(column=column)
        except:
            return HttpResponseRedirect(reverse('article:article_titles'))
    else:
        articles_title = articles

    # 文章分页
    paginator = Paginator(articles_title, 3)
    page_number = request.GET.get('page')
    # try:
    #     current_page = paginator.page(page_number)
    #     articles = current_page.object_list
    try:
        page_obj = paginator.get_page(page_number)
        articles = page_obj.object_list
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
        articles = page_obj.object_list
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
        articles = page_obj.object_list

    # 获取分类列表
    columns = User.objects.get(id=1).article_column.all()
    context = {
        "blog": 'active',
        "articles": articles,
        "page": page_obj,
        "columns": columns,
    }
    if column_name:
        context['active'] = column_name
    return render(request, "article/front/article_titles.html", context=context)


def article_content(request, aid, slug):
    article = get_object_or_404(ArticlePost, id=aid, slug=slug)

    # 特殊类型文章
    if article.showtype == '1':
        if request.user == 'AnonymousUser' or not ArticlePost.is_special_user(request.user.id):
            return HttpResponseRedirect(reverse('article:article_titles'))
        if request.method == "POST":  # 仅特殊文章可以评论
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.article = article
                new_comment.commentator = request.user
                new_comment.save()
            else:
                return render(request, "404.html")
        else:
            comment_form = CommentForm()

    if request.user.id != 1:
        article.viewed += 1
    article.save()
    context = {
        "article": article,
        "blog": 'active',
    }
    # 甜品站文章
    if article.showtype == '1':
        context['dessert'] = 'active'
        del context['blog']
        context['form'] = comment_form
    return render(request, "article/front/article_content.html", context=context)


@login_required
def dessert(request):
    if ArticlePost.is_special_user(request.user.id):
        articles = User.objects.get(id=1).article.filter(showtype='1')
        articles_title = articles
        paginator = Paginator(articles_title, 5)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
            articles = current_page.object_list
        except PageNotAnInteger:
            current_page = paginator.page(1)
            articles = current_page.object_list
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
            articles = current_page.object_list
        # 获取分类列表
        columns = User.objects.get(id=1).article_column.all()
        context = {
            "dessert": 'active',
            "articles": articles,
            "page": current_page,
            "columns": columns,
        }
        return render(request, "article/front/article_titles.html", context=context)
    else:
        return render(request, "404.html")
