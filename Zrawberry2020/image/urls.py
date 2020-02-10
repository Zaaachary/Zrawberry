from django.urls import path, re_path
from . import views

app_name = "images"

urlpatterns = [
    path('', views.PicList.as_view(), name='pic_list'),
    re_path('pic/upload/$', views.PicUpload.as_view(), name='pic_upload'),
    re_path('pic/(?P<pk>\d+)/$', views.PicDetail.as_view(), name='pic_detail'),
]
