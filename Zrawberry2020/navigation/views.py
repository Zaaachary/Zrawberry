from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from .models import LinkBox
from .forms import LinkForm


def navigation_index(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "LinkBox"):
            context = {
                'LBlist': request.user.LinkBox.all()
            }
    return render(request, "navigation/front/nav_index.html", context=context)


@login_required
@csrf_exempt
def navigation_list(request):
    if request.method == 'GET':
        LBlist = request.user.LinkBox.all()
        context = {
            'LBlist': LBlist,
            'LinkForm': LinkForm,
        }
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

