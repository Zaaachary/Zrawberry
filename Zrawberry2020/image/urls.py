from django.urls import path, re_path
from . import views

app_name = "images"

urlpatterns = [
    path('', views.PicList.as_view(), name='pic_list'),
    path('upload-modelform/', views.picture_modelform_upload, name='model_form_upload'),
    path('upload-ajax/', views.picture_ajax_upload, name='ajax_upload'),
    path('delete-ajax/', views.picture_delete, name='pic_delete'),
    re_path('pic/upload/$', views.PicUpload.as_view(), name='pic_upload'),
    re_path('pic/(?P<pk>\d+)/$', views.PicDetail.as_view(), name='pic_detail'),
]
