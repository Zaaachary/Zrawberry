from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.template.defaultfilters import filesizeformat
from django.contrib.auth.decorators import login_required

from .models import Picture
from .forms import PictureUploadForm


class PicList(ListView):
    queryset = Picture.objects.all().order_by('-date')
    # ListView默认Context_object_name是object_list
    context_object_name = 'picture_list'
    # 默认template_name = 'pic_upload/picture_list.html'
    template_name = 'image/back/image_manage.html'

    paginate_by = 6

    form = PictureUploadForm
    extra_context = {
        'form': form,
        'pic': 'active',
    }


class PicDetail(DetailView):
    model = Picture
    # DetailView默认Context_object_name是picture

    # 下面是DetailView默认模板，可以换成自己的
    template_name = 'image/test/picture_detail.html'


# 视图
class PicUpload(CreateView):
    model = Picture

    # 可以通过fields选项自定义需要显示的表单
    fields = ['title', 'image']

    # CreateView默认Context_object_name是form。

    # 下面是CreateView默认模板，可以换成自己模板
    template_name = 'image/test/picture_form.html'


# 使用modelform上传
def picture_modelform_upload(requset):
    if requset.method == "POST":
        form = PictureUploadForm(requset.POST, requset.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('images:pic_list'))
    else:
        form = PictureUploadForm()
        context = {
            'form': form,
        }

    return render(requset, 'image/back/image_manage.html', context=context)


@login_required
@require_POST
def picture_ajax_upload(request):
    form = PictureUploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        pictures = Picture.objects.all().order_by('-id')
        data = []
        for pic in pictures:
            data.append(
                {"title": pic.title,
                 "url": pic.image.url,
                 "size": filesizeformat(pic.image.size),
                 "date": pic.date,
                 }
            )
        return JsonResponse(data, safe=False)
    else:
        data = {'error_msg': '仅支持jpg, png格式'}
        return JsonResponse(data)



@login_required
@require_POST
def picture_delete(request):
    try:
        image_id = request.POST['image_id']
        pic = Picture.objects.get(id=image_id)
        pic.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")



