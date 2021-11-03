from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from .forms import ListingForm
from .mixin import SuperUserAccsesMixin, AuthorsAccessMixin
from django.views.generic import ListView, DeleteView
from blog.models import Article
from django.contrib.auth import logout, login
from .choices import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import MyUser
from . import forms
from . import helper
from django.contrib import messages


def register_view(request):
    form = forms.RegisterForm
    if request.method == "POST":
        try:
            if "mobile" in request.POST:
                mobile = request.POST.get('mobile')
                user = MyUser.objects.get(mobile=mobile)
                # send otp
                otp = helper.get_random_otp()
                helper.send_otp(mobile, otp)
                # save otp
                print(otp)
                user.otp = otp
                user.save()
                request.session['user_mobile'] = user.mobile
                messages.info(request, ' کد ارسال شده را وارد کنید و سپس روی کلید "ورود / ثبت نام" کلیک کنید.')
                return HttpResponseRedirect(reverse('verify'))


        except MyUser.DoesNotExist:
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # send otp
                otp = helper.get_random_otp()
                helper.send_otp(mobile, otp)
                # save otp
                print(otp)
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                messages.info(request, ' کد ارسال شده را وارد کنید و سپس روی کلید "ورود / ثبت نام" کلیک کنید.')
                return HttpResponseRedirect(reverse('verify'))
    return render(request, 'registration/register.html', {'form': form})


def verify(request):
    try:
        mobile = request.session.get('user_mobile')
        user = MyUser.objects.get(mobile=mobile)
        if request.method == "POST":
            # check otp expiration
            if not helper.check_otp_expiration(user.mobile):
                messages.error(request, 'کد یکبار مصرف شما منقضی شده...لطفا دوباره سعی کنید!!!')
                return HttpResponseRedirect(reverse('register_view'))
            if user.otp != int(request.POST.get('otp')):
                messages.error(request, 'کد وارد شده با کد ارسال شده فرق دارد...لطفا دوباره سعی کنید!!!')
                return HttpResponseRedirect(reverse('verify'))
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'خوش آمدید :) با موفقیت وارد سایت شدید')
            return HttpResponseRedirect(reverse('account:upload'))
        return render(request, 'registration/verify.html', {'mobile': mobile})
    except MyUser.DoesNotExist:
        messages.error(request, "Error accorded, try again.")
        return HttpResponseRedirect(reverse('register_view'))


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'خارج شدید, متشکر از اینکه مدتی از وقت خود را به ما اختصاص دادید.')


class ArticleList(AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all().order_by('-publish')
        else:
            return Article.objects.filter(author=self.request.user).order_by('-publish')


class ArticleDelete(SuperUserAccsesMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = "registration/delete.html"


def upload(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_superuser:
                a = form.save(commit=False)
                a.status = 'p'
                a.save()
            else:
                new_listing = form.save(commit=False)
                new_listing.author = request.user
                new_listing.status = 'i'
                new_listing.save()
                messages.success(request,
                                 'ملک شما با موفقیت ثبت شد پس از برررسی  , در سایت نمایش داده می شود "با تشکر از '
                                 'صبوری شما"')
            return redirect('account:home')
        else:
            messages.error(request, 'خطا در ثبت آگهی !!! با مدیر سایت ارتباط برقرار کنید.')
            return redirect("account:upload")
    else:
        form = ListingForm()
        if not request.user.is_authenticated:
            messages.error(request, 'برای ثبت آگهی ابتدا باید وارد سایت شوید')
            return redirect('register_view')
    context = {
        'conditions_choices': conditions_choices,
        'document_choices': document_choices,
        'type_choices': type_choices,
        'contract_choices': contract_choices,
        'bedroom_choices': bedroom_choices,
        'direction_choices': direction_choices,
        'covering_choices': covering_choices,
        'cooling_choices': cooling_choices,
        'heating_choices': heating_choices,
        'water_choices': water_choices,
        'construction_choices': construction_choices,
        'advertiser_choices': advertiser_choices,
        "form": form,
    }
    return render(request, "registration/submit.html", context)
