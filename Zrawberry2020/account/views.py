from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login  # 内置的用户认证和管理
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt

from .forms import LoginForm, RegistrationForm, UserProfileForm, UserForm, UserInfoForm
from .models import UserProfile, UserInfo


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:  # 如果检验正确则未一个user实例 否则None
                login(request, user)
            else:
                return HttpResponse("用户名不存在或密码错误")
        else:
            return HttpResponse("无效登录")

    if request.method == "GET":
        login_form = LoginForm()
        context = {
            "form": login_form
        }
        return render(request, "account/login.html", context=context)


def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and userprofile_form.is_valid():
            new_user = user_form.save(commit=False)  # 仅生成数据对象,此时里面还没有设置password
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponseRedirect(reverse("account:user_login"))
        else:
            return HttpResponse("注册失败，用户名或邮箱已经被使用 或 两次密码不一致！请重新<a href="+reverse("account:user_register")+'>注册</a>')
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        context = {
            "form": user_form,
            "profile": userprofile_form
        }
        return render(request, "account/register.html", context=context)


@login_required()
def myself(request):
    userprofile = UserProfile.objects.get(user=request.user) if \
        hasattr(request.user, 'userprofile') else \
        UserProfile.objects.create(user=request.user)
    if hasattr(request.user, 'userinfo'):
        userinfo = UserInfo.objects.get(user=request.user)
    else:
        userinfo = UserInfo.objects.create(user=request.user)
    context = {"user": request.user,
               "userinfo": userinfo,
               "userprofile": userprofile,
               "account": 'active',
               }
    return render(request, "account/myself.html", context=context)


@login_required()
def myself_edit(request):
    userprofile = UserProfile.objects.get(user=request.user) if \
        hasattr(request.user, 'userprofile') else \
        UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if \
        hasattr(request.user, 'userinfo') else \
        UserInfo.objects.create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and userinfo_form.is_valid() and userprofile_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            request.user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.wechat = userprofile_cd['wechat']
            for k, v in userinfo_cd.items():
                if k is not 'photo':
                    setattr(userinfo, k, v)
            request.user.save()
            userprofile.save()
            userinfo.save()
            return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth,
                                                    "wechat": userprofile.wechat})
        userinfo_form = UserInfoForm(initial={"school": userinfo.school,
                                              "company": userinfo.company,
                                              "specialty": userinfo.specialty,
                                              "address": userinfo.address,
                                              "aboutme": userinfo.aboutme})
        context = {
            "user_form": user_form,
            "userinfo_form": userinfo_form,
            "userprofile_form": userprofile_form,
            "userinfo": userinfo,
            "account": 'active',
        }
        return render(request, "account/myself_edit.html", context=context)


@login_required
@xframe_options_exempt
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user) if \
            hasattr(request.user, 'userinfo') else \
            UserInfo.objects.create(user=request.user)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/imagecrop.html')


@login_required
def dashboard(request):
    return render(request, 'common/back_base.html', context={"account": 'active', })
