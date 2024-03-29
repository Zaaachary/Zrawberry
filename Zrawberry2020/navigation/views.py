from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from article.views import get_common_context
from .models import LinkBox
from .forms import LinkForm


@login_required
@csrf_exempt
def navigation_list(request):
    """盒子内的链接"""
    if request.method == 'GET':
        LBlist = LinkBox.objects.filter(owner=request.user).order_by('created')
        context = {
            'LBlist': LBlist,
            'LinkForm': LinkForm,
            'links': 'active',
        }
        get_common_context(context)
        return render(request, "navigation/back/nav_list.html", context=context)
    elif request.method == "POST":
        if request.POST['op'] == "add_url":
            # 添加链接
            box_id = request.POST['box_id']
            sitename = request.POST['sitename']
            url = request.POST['url']
            box = LinkBox.objects.get(owner_id=request.user.id, id=box_id)
            urldict = box.str2dict()
            # 检查是否已存在此站点
            if sitename in urldict.keys():
                return HttpResponse('2')
            else:
                urldict[sitename] = url
                box.urls = LinkBox.dict_jsontr(urldict)
                box.save()
                return HttpResponse('1')
        elif request.POST['op'] == "del_url":
            # 删除链接
            box_id = request.POST['box_id']
            sitename = request.POST['sitename']
            box = LinkBox.objects.get(owner_id=request.user.id, id=box_id)
            urldict = box.str2dict()
            try:
                urldict.pop(sitename)
                box.urls = LinkBox.dict_jsontr(urldict)
                box.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        elif request.POST['op'] == 'update_url':
            # 修改链接
            box_id = request.POST['box_id']
            old_sitename = request.POST['old_sitename']
            new_sitename = request.POST['new_sitename']
            new_link = request.POST['url']
            box = LinkBox.objects.get(owner_id=request.user.id, id=box_id)
            urldict = box.str2dict()
            if old_sitename in urldict:
                del urldict[old_sitename]
                urldict[new_sitename] = new_link
                box.urls = LinkBox.dict_jsontr(urldict)
                box.save()
                return HttpResponse("1")
            else:
                return HttpResponse("2")
        else:
            return HttpResponse("2")


@login_required
@csrf_exempt
def navigation_box(request):
    if request.method == 'GET':
        LBlist = LinkBox.objects.filter(owner=request.user).order_by('created')
        context = {
            'LBlist': LBlist,
            'boxes': 'active',
        }
        get_common_context(context)
        return render(request, "navigation/back/nav_box.html", context=context)
    elif request.method == "POST":
        if request.POST['op'] == "add_box":
            # 添加盒子
            boxname = request.POST['boxname']
            if type(boxname) is str and len(boxname)>0:
                box = LinkBox(boxname=boxname, owner_id=request.user.id)
                box.save()
                return HttpResponse('1')
            else:
                return HttpResponse('2')
        elif request.POST['op'] == "del_box":
            # 删除盒子
            box_id = request.POST['boxid']
            box = LinkBox.objects.get(owner_id=request.user.id, id=box_id)
            try:
                box.delete()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        elif request.POST['op'] == "update_box":
            # 修改盒子名称
            box_id = request.POST['boxid']
            boxname = request.POST['boxname']
            if type(boxname) is str and len(boxname)>0:
                box = LinkBox.objects.get(owner_id=request.user.id, id=box_id)
                box.boxname=boxname
                box.save()
                return HttpResponse('1')
            else:
                return HttpResponse('2')
        else:
            return HttpResponse("2")

def navigation_index(request):
    context = {}
    if request.user.is_authenticated:
        if hasattr(request.user, "LinkBox"):
            context['LBlist'] = request.user.LinkBox.all()
    get_common_context(context)
    return render(request, "navigation/front/nav_index.html", context=context)


class FrontendView(ListView):
    # template_name = "navigation/back/nav_box.html"
    template_name = "navigation/front/nav_index.html"
    context_object_name = 'LBlist'

    def get_queryset(self):
        # self.request.user
        if self.request.user.is_authenticated:
            # return LinkBox.objects.filter(owner=self.request.user).order_by('-created')
            return LinkBox.objects.filter(owner=self.request.user)
        else:
            return None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        get_common_context(context)
        return context

